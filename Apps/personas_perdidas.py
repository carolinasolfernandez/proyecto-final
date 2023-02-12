import math
import argparse
'''
Recupera persosas perdidas por cruce u oclusion parcial. 
Toma el x,y donde se detecto por ultima vez y busca por una cantidad maxima de frames
si encuentra a la personas en un radio menor al definido.
Solo busca personas que aparecen nuevas en el radio - no toma en cuenta las que ya existian de antes
En el caso de que aparezca una persona en la posicion donde se perdio la anterior, completa todos los frames faltantes
con una persona en esa posicion y un bb igual al nuevo

La salida es un archivo con las detecciones existentes y nuevas
'''
#python personas_perdidas.py ../resultados/siam-mot/59/20230207-195238/20230207-195238-out.txt ./results.txt


radius = 10
max_miss_frames = 215

def is_point_in_circle(x1, y1, r, x2, y2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance < r


def read_file(input):
    frames = {}
    last_frame = 1
    # Read the ground truth data from a CSV file
    with open(input, "r") as file:
        for line in file:
            frame, id, x, y, width, height, prob, xx, yy, zz = line.split(', ')
            last_frame = frame
            frame, x, y, width, height, probability = int(frame), float(x), float(y), float(width), float(height), float(prob)

            if frame not in frames:
                frames[int(frame)] = [(id, x, y, width, height, prob, xx, yy, zz)]
            else:
                frames[int(frame)].append((id, x, y, width, height, prob, xx, yy, zz))
    return frames, last_frame


def find_people(frames):
    missing_people_frames = {}
    person_positions = {}
    possible_missing_people = {}
    associations_ids = {}

    for frame in frames:
        people = frames[frame]

        if frame == 1:
            for person in people: 
                id, x, y, width, height, prob, xx, yy, zz = person
                person_positions[id] = (x, y)
        else:
            people_ids = []
            new_people = []

            for person in people:
                id, x, y, width, height, prob, xx, yy, zz = person

                people_ids.append(id)

                    
            missing_ids = set(person_positions.keys()) - set(people_ids)

            for missing_id in missing_ids:
                if missing_id not in possible_missing_people:
                    possible_missing_people[missing_id] = (1, person_positions[missing_id][0], person_positions[missing_id][1], frame)
                else:
                    number_of_frame = possible_missing_people[missing_id][0] + 1
                    last_frame = possible_missing_people[missing_id][3]

                    if number_of_frame > max_miss_frames:
                        del possible_missing_people[missing_id]
                        del person_positions[missing_id]
                    else:
                        possible_missing_people[missing_id] = (number_of_frame, person_positions[missing_id][0], person_positions[missing_id][1], last_frame)

            for person in people:
                id, x, y, width, height, prob, xx, yy, zz = person

                if id in person_positions:
                    person_positions[id] = (x, y)
                else:
                    is_new_person = True
                    found_missing_person = None
                    for id_missing_person in possible_missing_people:
                        missing_person = possible_missing_people[id_missing_person]
                        circleX = missing_person[1]
                        circleY = missing_person[2]
                        missing_frame = missing_person[3]

                        if is_point_in_circle(circleX, circleY, radius, x, y):
                            person_positions[id] = (x, y)
                            is_new_person = False
                            found_missing_person = id_missing_person
                            associations_ids[id] = id_missing_person

                            for i in range(missing_frame, frame):
                                if i not in missing_people_frames:
                                    missing_people_frames[i] = []
                                missing_people_frames[i].append(person)

                            break

                    if is_new_person:
                        new_people.append(person)
                    else:
                        del possible_missing_people[found_missing_person]
                        del person_positions[found_missing_person]

            for new_person in new_people:
                person_positions[new_person[0]] = (new_person[1], new_person[2])
    return missing_people_frames, associations_ids

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The path to the input file")
    parser.add_argument("output_file", help="The path to the output file")
    args = parser.parse_args()

    frames, last_frame = read_file(args.input_file)
    missing_people_frames, associations_ids = find_people(frames)

    with open(args.output_file, "w") as f_out:
        for frame in range(1, int(last_frame)+1):
            if frame in missing_people_frames:
                for person in missing_people_frames[frame]:
                    id, x, y, width, height, prob, xx, yy, z = person
                    while id in associations_ids: # asigno el id original
                        id = associations_ids[id]
                    if x > 1 and y > 1:
                        f_out.write(', '.join([str(frame), id, str(x), str(y), str(width), str(height), str(prob), str(xx), str(yy), str(z)]))
            
            if frame in frames:
                for person in frames[frame]:
                    id, x, y, width, height, prob, xx, yy, z = person
                    while id in associations_ids:
                        id = associations_ids[id]
                    f_out.write(', '.join([str(frame), id, str(x), str(y), str(width), str(height), str(prob), str(xx), str(yy), str(z)]))

    #print(missing_people_frames)