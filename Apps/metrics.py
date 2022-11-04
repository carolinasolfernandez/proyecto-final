
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
        
        
    def getErrorObjectDetectionByFrame(self):
        datasetCountObjByFrame = {}
        gtCountObjByFrame = {}
        errorFrame = []
        frames=[]

        for r in self.dataset:
            frame=r.get('frame')
            datasetCountObjByFrame[frame]=datasetCountObjByFrame.get(frame, 0)+1

        for r in self.gt:
            frame = r.get('frame')
            gtCountObjByFrame[frame]=gtCountObjByFrame.get(frame, 0)+1

        for frame in datasetCountObjByFrame:
            countDataset=datasetCountObjByFrame.get(frame)
            countGT=gtCountObjByFrame.get(frame)
            error=abs((countDataset-countGT)/countDataset)
            errorFrame.append(error*100)
            frames.append(frame)

        averageError=statistics.mean(errorFrame)
        print("Average obj count error [%]: "+str(averageError))
        return errorFrame, averageError, frames



class Utils():
    def __init__(self, outFolder):
        self.outFolder = outFolder

    def getData(self, file):
        data=[]
        reader = csv.reader(open(file))
        for row in reader:
            data.append({
                "frame":    row[0],
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

    def writeResult(self, outFile, brief, header, data):
        with open(self.outFolder+"/"+outFile, 'a+', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
            myfile.write(brief+"\n")
            wr.writerow(header)
            wr.writerow(data)
            myfile.write("-----------\n")


    def plot(self, outFile, x, y, title, xlabel, ylabel):
        plt.plot(x, y)
        plt.title(title)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.savefig(self.outFolder+"/"+outFile)
        plt.show() 


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
    errorByFrame, averageError, frames=metrics.getErrorObjectDetectionByFrame()
    

    utils.plot('error_obj.png', frames, errorByFrame, 'Person errror count by Frame', 'Frame', 'Error %')
    utils.writeResult("metrics.txt", "Error Detecciones por Frame Promedio [%]: "+str(averageError), frames, errorByFrame)
