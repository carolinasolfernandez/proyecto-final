
import csv
import statistics
import sys, getopt
from munkres import Munkres
from scipy.optimize import linear_sum_assignment
import numpy as np
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
        self.iou_threshold = 0.2

    def getErrorObjectDetectionByFrameWithIOU(self, gt_bboxesFrame, det_bboxesFrame):
        precision_frame=[]
        recall_frame=[]
        f1_score_frame=[]
        for f in range(1, self.frames+1):
            gt_bboxes = gt_bboxesFrame.get(f, [])
            det_bboxes = det_bboxesFrame.get(f, [])
            #gt_bboxes = [[10, 20, 30, 40], [50, 60, 70, 80], [90, 100, 110, 120]]
            #det_bboxes = [[15, 25, 35, 45], [55, 65, 75, 85], [95, 105, 115, 125]]

            # Calculate IoU between all pairs of bounding boxes
            iou_matrix = np.zeros((len(gt_bboxes), len(det_bboxes)))
            for i, gt_bbox in enumerate(gt_bboxes):
                for j, det_bbox in enumerate(det_bboxes):
                    # Calculate the coordinates of the intersection
                    x1 = max(gt_bbox[0], det_bbox[0])
                    y1 = max(gt_bbox[1], det_bbox[1])
                    x2 = min(gt_bbox[2], det_bbox[2])
                    y2 = min(gt_bbox[3], det_bbox[3])

                    # Calculate the area of intersection
                    intersection = max(0, x2 - x1) * max(0, y2 - y1)

                    # Calculate the area of union
                    gt_area = (gt_bbox[2] - gt_bbox[0]) * (gt_bbox[3] - gt_bbox[1])
                    det_area = (det_bbox[2] - det_bbox[0]) * (det_bbox[3] - det_bbox[1])
                    union = gt_area + det_area - intersection

                    # Calculate the IoU
                    iou_matrix[i, j] = intersection / union
            
            # Apply the Hungarian algorithm to find the optimal assignment
            row_ind, col_ind = linear_sum_assignment(-iou_matrix)

            tp = len([i for i in range(len(row_ind))  if iou_matrix[row_ind[i], col_ind[i]] >= self.iou_threshold])
            fp = len(det_bboxes) - tp
            fn = len(gt_bboxes) - tp
            
            if tp == 0 and fp == 0:
                precision=1
            else:        
                precision = tp / (tp + fp)

            if tp == 0 and fn == 0:
                recall = 1
            else:        
                recall = tp / (tp + fn)
            
            if precision == 0 and recall == 0:
                f1_score = 0
            else:
                f1_score = 2 * (precision * recall) / (precision + recall)


            precision_frame.append(precision)
            recall_frame.append(recall)
            f1_score_frame.append(f1_score)
        
        averagePrecision=statistics.mean(precision_frame)
        averageRecall=statistics.mean(recall_frame)
        averageF1=statistics.mean(f1_score_frame)
        print("Average Precision: "+str(averagePrecision), "Recall: "+str(averageRecall), "F1 Score: "+str(averageF1))

        return precision_frame, recall_frame, f1_score_frame, averagePrecision, averageRecall, averageF1

    def getErrorObjectDetectionByFrame(self):
        datasetCountObjByFrame = {}
        gtCountObjByFrame = {}
        errorFrame = []
        detectedObjs =[]
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
            detectedObjs.append(countDataset)
            expectedObjs.append(countGT)

        averageError=statistics.mean(errorFrame)
        return detectedObjs, expectedObjs, errorFrame, averageError, list(range(1, self.frames+1))


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

    def getBB(self, data):
        bb = {}
        for r in data:
            x1D = float(r.get('x'))
            if x1D < 0:
                x1D = 0
            y1D = float(r.get('y'))
            if y1D < 0:
                y1D = 0
            x2D = x1D + float(r.get('width'))
            y2D = y1D + float(r.get('height'))
            bbData = [x1D, y1D, x2D, y2D]
            frame = r.get('frame')
            if frame not in bb.keys():
                bb[frame] = []
            bb[frame].append(bbData)
        return bb

    def writeResult(self, outFile, brief,  detected, expected, header=[], errors=[], precision=[], recall=[], f1_score=[]):
        detected.insert(0, "detected")
        expected.insert(0, "expected")
        with open(self.outFolder+"/"+outFile, 'a+', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
            myfile.write(brief+"\n")
            if len(header):
                header.insert(0, "frames")
                wr.writerow(header)
            wr.writerow(detected)
            wr.writerow(expected)
            if len(errors):
                errors.insert(0, "error")
                wr.writerow(errors)
            
            if len(precision):
                precision.insert(0, "precision")
                wr.writerow(precision)
            
            if len(recall):
                recall.insert(0, "recall")
                wr.writerow(recall)
            
            if len(f1_score):
                f1_score.insert(0, "f1_score")
                wr.writerow(f1_score)
            myfile.write("-----------\n")


    def plot(self, outFile, detected, expected, f1, precision, recall, x, title, xlabel, ylabel):
        fig, ax = plt.subplots()
        ax.set_xlabel(xlabel)

        # Grafico Error
        ax.plot(x, f1, label = "F1 Score", color='tab:red', linestyle = 'dotted')
        ax.plot(x, precision, label = "Precision", color='tab:green', linestyle = 'dotted')
        ax.plot(x, recall, color='tab:purple', linestyle = 'dotted', label = "Recall")
        ax.tick_params(axis='y')

        ax.set_ylabel("Metricas")
        # Grafico Valor esperado - detectado
        ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
        ax2.set_ylabel(ylabel)  
        ax2.plot(x, detected, color='tab:blue', label = "Detectadas")
        ax2.plot(x, expected, color='tab:orange' , label = "Esperadas")
        ax.legend(loc=0)
        fig.tight_layout() 
        plt.legend()
        plt.subplots_adjust(top=0.95)
        plt.gcf().set_size_inches(10, 7)
        plt.title(title)
        plt.savefig(self.outFolder+"/"+outFile) 
        #plt.show()


    def plotSinError(self, outFile, detected, expected, yDetected, yExpected, title, xlabel, ylabel):
        plt.figure()
        plt.plot(detected, yDetected, color='tab:blue', label="Detectadas")
        plt.plot(expected, yExpected, color='tab:orange', label="Esperadas")
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

    datasetBB = utils.getBB(dataset)
    gtBB = utils.getBB(gt)

    metrics = Metrics(dataset, gt)
    detected, expected, errorByFrame, averageError, frames=metrics.getErrorObjectDetectionByFrame()
    
    precision_frame, recall_frame, f1_score_frame, averagePrecision, averageRecall, averageF1 = metrics.getErrorObjectDetectionByFrameWithIOU(gtBB, datasetBB)

    utils.plot('person_count.png', detected, expected, f1_score_frame, precision_frame, recall_frame, frames, 'Detecciones por frame', 'Frame', 'Personas detectadas/esperadas')
    utils.writeResult("metrics.txt", "F1 Score Promedio: "+str(averageF1)+"\nPrecision Promedio: "+str(averagePrecision)+"\nRecall Promedio: "+str(averageRecall),  detected, expected, frames, [], precision_frame, recall_frame, f1_score_frame)

    #utils.writeResult("metrics.txt", "Error Detecciones por Frame Promedio [%]: "+str(averageF1),  detected, expected, frames, f1_score_frame,  precision_frame, recall_frame)

    detected, expected, maxDetected, maxExpected = metrics.getMomentoMasConcurrido()
    utils.plotSinError('mas_concurrido.png', detected, expected, maxDetected, maxExpected, "Frames mas concurridos", 'Frames', 'Personas detectadas/esperadas')
    utils.writeResult("metrics.txt", "Frames mas concurridos. Max Personas Detectadas: "+str(maxDetected[0])+" vs Esperadas: "+str(maxExpected[0]), detected, expected)
