
import csv
import statistics
import sys, getopt
import matplotlib.pyplot as plt

# python metrics.py -d ../resultados/yolox/20221104-162639/20221104-162639-out.txt -g ../resultados/yolox/20221104-162639/gt.txt -o ../resultados/yolox/20221104-162639

class Metrics():
    # init method or constructor
    def __init__(self,  dataset, gt):
        self.dataset = dataset
        self.gt = gt
        datasetFrames= dataset[-1:][0].get("frame")
        gtFrames= gt[-1:][0].get("frame")
        self.frames = int(max(datasetFrames, gtFrames))
        
        
    def getErrorObjectDetectionByFrame(self):
        datasetCountObjByFrame = {}
        gtCountObjByFrame = {}
        errorFrame = []
        realObjs =[]
        expectedObjs =[]


        for r in self.dataset:
            frame=r.get('frame')
            datasetCountObjByFrame[frame]=datasetCountObjByFrame.get(frame, 0)+1

        for r in self.gt:
            frame = r.get('frame')
            gtCountObjByFrame[frame]=gtCountObjByFrame.get(frame, 0)+1


        for frame in range(1, self.frames+1):
            countDataset=datasetCountObjByFrame.get(frame, 0)
            countGT=gtCountObjByFrame.get(frame, 0)
            error=abs(countDataset-countGT)/max(countDataset, countGT)
            errorFrame.append(error*100)
            realObjs.append(countDataset)
            expectedObjs.append(countGT)

        averageError=statistics.mean(errorFrame)
        print("Average obj count error [%]: "+str(averageError))
        return realObjs, expectedObjs, errorFrame, averageError, list(range(1, self.frames+1))


    def getMomentoMasConcurrido(self):
        datasetCountObjByFrame = {}
        gtCountObjByFrame = {}


        for r in self.dataset:
            frame=r.get('frame')
            datasetCountObjByFrame[frame]=datasetCountObjByFrame.get(frame, 0)+1

        for r in self.gt:
            frame = r.get('frame')
            gtCountObjByFrame[frame]=gtCountObjByFrame.get(frame, 0)+1

        maximumObjsDataset = max(datasetCountObjByFrame.values())
        framesDataMasConcurridos = [key for key, value in datasetCountObjByFrame.items() if value == maximumObjsDataset]

        maximumObjsGT = max(gtCountObjByFrame.values())
        framesGTMasConcurridos = [key for key, value in gtCountObjByFrame.items() if value == maximumObjsGT]

        return framesDataMasConcurridos, framesGTMasConcurridos, [maximumObjsDataset] * len(framesDataMasConcurridos), [maximumObjsGT] * len(framesGTMasConcurridos)


class Utils():
    def __init__(self, outFolder):
        self.outFolder = outFolder

    def getData(self, file):
        data=[]
        reader = csv.reader(open(file))
        for row in reader:
            data.append({
                "frame":    int(row[0]),
                "obj":      row[1],
                "x":        row[2],
                "y":        row[3],
                "width":    row[4],
                "height":   row[5],
                "score":    row[6],
                "xx":       row[7],
                "yy":       row[8],
                "zz":       row[9]
            })
        return data

    def writeResult(self, outFile, brief,  real, expected, header=[], errors=[]):
        real.insert(0, "real")
        expected.insert(0, "expected")
        with open(self.outFolder+"/"+outFile, 'a+', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
            myfile.write(brief+"\n")
            if len(header):
                header.insert(0, "type")
                wr.writerow(header)
            wr.writerow(real)
            wr.writerow(expected)
            if len(errors):
                errors.insert(0, "error")
                wr.writerow(errors)
            myfile.write("-----------\n")


    def plot(self, outFile, real, expected, error, x, title, xlabel, ylabel):
        fig, ax = plt.subplots()
        ax.set_xlabel(xlabel)

        # Grafico Error
        ax.set_ylabel("Error relativo %", color='tab:red')
        ax.plot(x, error, label = "error", color='tab:red', linestyle = 'dotted')
        ax.tick_params(axis='y', labelcolor='tab:red')

        # Grafico Valor esperado - real
        ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
        ax2.set_ylabel(ylabel)  
        ax2.plot(x, real, label = "real")
        ax2.plot(x, expected, label = "esperado")

        fig.tight_layout() 
        plt.legend()
        plt.title(title)
        plt.savefig(self.outFolder+"/"+outFile) 
        #plt.show()


    def plotSinError(self, outFile, real, expected, yReal, yExpected, title, xlabel, ylabel):
        plt.plot(real, yReal, label="Real")
        plt.plot(expected, yExpected, label="Esperado")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend()
        plt.savefig(self.outFolder+"/"+outFile)
        #plt.show() 


def main(argv):
    datasetFile = ''
    gtFile = ''
    outFolder = '.'
    try:
        opts, args = getopt.getopt(argv,"ho:d:g:",[])
    except getopt.GetoptError:
        print("metrics.py -d <datasetFile> -g <gtFile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("metrics.py -d <datasetFile> -g <gtFile> -o <outFolder>")
            sys.exit()
        elif opt in ("-d"):
            datasetFile = arg
        elif opt in ("-g"):
            gtFile = arg
        elif opt in ("-o"):
            outFolder = arg
    return datasetFile, gtFile, outFolder


if __name__ == "__main__":
    datasetFile, gtFile, outFolder= main(sys.argv[1:])
    
    utils = Utils(outFolder)

    dataset= utils.getData(datasetFile)
    gt= utils.getData(gtFile)

    metrics = Metrics(dataset, gt)
    real, expected, errorByFrame, averageError, frames=metrics.getErrorObjectDetectionByFrame()
    

    utils.plot('person_count.png', real, expected, errorByFrame, frames, 'Error deteccion por frame', 'Frame', 'Personas detectadas')
    utils.writeResult("metrics.txt", "Error Detecciones por Frame Promedio [%]: "+str(averageError),  real, expected, frames, errorByFrame)

    real, expected, maxReal, maxExpected = metrics.getMomentoMasConcurrido()
    utils.plotSinError('mas_concurrido.png', real, expected, maxReal, maxExpected, "Frames mas concurridos", 'Frames', 'Personas detectadas')
    utils.writeResult("metrics.txt", "Frames mas concurridos. Max Personas Real: "+str(maxReal[0])+" vs Esperado: "+str(maxExpected[0]), real, expected)
