def printStatistics(distanceHistogram, histogramSum = -1):
    if histogramSum == -1:
        histogramSum = 0

        for n in distanceHistogram:
            histogramSum += n

    # Calculate median distance from histogram
    
    medianIndex = histogramSum // 2
    histogramIndex = 0
    
    for i, bucket in enumerate(distanceHistogram):
        histogramIndex += bucket
        
        if histogramIndex >= medianIndex:
            median = i
            break
    
    print("Median distance: " + str(median))
    
    # Calculate mean distance from histogram
    
    mean = 0.0
    for i in xrange(len(distanceHistogram)):
        mean += i * distanceHistogram[i]
    
    mean /= histogramSum
    print("Mean distance: " + str(mean))
    
    # Diameter (= max of all distances)
    
    for i, bucket in reversed(list(enumerate(distanceHistogram))):
        if bucket != 0:
            diameter = i
            break
    
    print("Diameter: " + str(diameter))
    
    # Effective diameter
    
    edIndex = int(histogramSum * 0.9)
    histogramIndex = 0
    
    for i, bucket in enumerate(distanceHistogram):
        histogramIndex += bucket
        
        if histogramIndex >= edIndex:
            effectiveDiameter = i
            break
    
    print("Effective diameter: " + str(effectiveDiameter))
