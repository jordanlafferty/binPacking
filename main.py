import timeit


def fixOrder(m1, m2, m3):
    # rearranges the order of the length, width and height
    # returning them in order from largest to smallest
    if m1 >= m2:
        if m1 >= m3:
            l = m1
            if m2 >= m3:
                w = m2
                h = m3
            else:
                w = m3
                h = m2
        else:
            l = m3
            w = m1
            h = m2
    elif m2 >= m1:
        if m2 >= m3:
            l = m2
            if m1 >= m3:
                w = m1
                h = m3
            else:
                w = m3
                h = m1
        else:
            l = m3
            w = m2
            h = m1

    return l, w, h


class Bin:
    def __init__(self, l, w, h):
        l, w, h = fixOrder(l, w, h)
        self.length = l
        self.width = w
        self.height = h
        self.volume = l * w * h
        self.binArr = []
        self.currBin = []

    def pack(self, boxArr):
        # this algorithm will take the most bins, but is the fastest

        count = 0  # keeps track of how many bins you will need
        newSide1 = self.length  # largest dimension of the packing bin
        newSide2 = self.width  # middle dimension of the packing bin
        newSide3 = self.height  # smallest dimension of the packing bin

        for i in range(len(boxArr)):
            # goes through every box and tries to put it in the current container
            aBox = boxArr[i]  # current box

            # making sure the box will actually currBin in the bin
            if aBox[0] <= self.length and aBox[1] <= self.width and aBox[2] <= self.height:
                # subtracts the current dimension available from the dimensions
                # of the current box you are trying to fit
                newSide1 = newSide1 - aBox[0]
                newSide2 = newSide2 - aBox[1]
                newSide3 = newSide3 - aBox[2]

                # if after subtracting the dimensions, none of the sides are 0,
                # you know that the box can currBin, so you can add it to the current bin
                if newSide1 >= 0 and newSide2 >= 0 and newSide3 >= 0:
                    # adding the box to the current bin
                    self.currBin.append(aBox)
                # if the current box can not fit in the bin
                else:
                    count += 1  # add to number of bins
                    # add the bin to the array that holds all the bins and their boxes
                    self.binArr.append(self.currBin)
                    self.currBin = []  # reset the current bin
                    self.currBin.append(aBox)  # add the current box in

                    # reset all the dimensions of the bin
                    newSide1 = self.length - aBox[0]
                    newSide2 = self.width - aBox[1]
                    newSide3 = self.height - aBox[2]

        # since all the boxes have gone into their bins, if there
        # are any boxes left in the current bin, add the current bin to array of bins
        if self.currBin:
            self.binArr.append(self.currBin)
            count += 1

        # print out each
        print("You need " + str(count) + " bins to fit the boxes")
        for i in range(len(self.binArr)):
            print(self.binArr[i])

    def pack2(self, boxArr):
        # this algorithm is the second fastest and will take the second amount of bins
        totalVolume = 0  # total volume of the boxes inside the current bin
        newSide1 = self.length  # largest dimension of the packing bin
        newSide2 = self.width  # middle dimension of the packing bin
        newSide3 = self.height  # smallest dimension of the packing bin
        i = 0

        # goes through every box to fit it into a bin
        while i < len(boxArr):
            aBox = boxArr[i]  # current box
            # makes sure box can initially fit
            if aBox[0] <= self.length and aBox[1] <= self.width and aBox[2] <= self.height:
                # subtracts the current dimension available from the dimensions
                # of the current box you are trying to fit
                newSide1 = newSide1 - aBox[0]
                newSide2 = newSide2 - aBox[1]
                newSide3 = newSide3 - aBox[2]

                # adds the box to the volume to see if it can initially fit
                totalVolume = totalVolume + aBox[0] * aBox[1] * aBox[2]
                if newSide1 >= 0 and newSide3 > 0 and totalVolume <= self.volume:
                    self.currBin.append(aBox)  # add box to current bin
                    # reset the sides not focused on
                    newSide2 = newSide2 + aBox[1]
                    newSide3 = newSide3 + aBox[2]

                # checks if the box can fit focused on the middle dimension, also making sure
                # that when the box added will be able to fit by limiting the volume to 3/4
                elif newSide2 >= 0 and newSide3 > 0 and totalVolume <= self.volume * 3 / 4:
                    self.currBin.append(aBox)  # add box to current bin
                    # reset the sides not focused on
                    newSide1 = newSide1 + aBox[0]
                    newSide3 = newSide3 + aBox[2]

                # checks if the box can fit focused on the middle dimension, also making sure
                # that when the box added will be able to fit by limiting the volume to 3/4
                elif newSide3 >= 0 and totalVolume <= self.volume * 3 / 4:
                    self.currBin.append(aBox)  # add box to current bin
                    # reset the sides not focused on
                    newSide1 = newSide1 + aBox[0]
                    newSide2 = newSide2 + aBox[1]

                # box can not fit into the current bi
                else:
                    # add the bin to the array that holds all the bins and their boxes
                    self.binArr.append(self.currBin)
                    self.currBin = []  # reset the current bin

                    totalVolume = 0  # reset volume
                    # reset all the dimensions of the bin
                    newSide1 = self.length
                    newSide2 = self.width
                    newSide3 = self.height

                    # resets i so that it will properly add the current box
                    i -= 1
            i += 1  # next box

        # since all the boxes have gone into their bins, if there
        # are any boxes left in the current bin, add the current bin to array of bins
        if self.currBin:
            self.binArr.append(self.currBin)

        # print out each
        print("You need " + str(len(self.binArr)) + " bins to fit the boxes")
        for i in range(len(self.binArr)):
            print(self.binArr[i])

    def pack3(self, boxArr):
        # this algorithm is the slowest but has the best solution
        totalVolume = 0  # total volume of the boxes inside the current bin
        newSide1 = self.length  # largest dimension of the packing bin
        newSide2 = self.width  # middle dimension of the packing bin
        newSide3 = self.height  # smallest dimension of the packing bin
        fitted = []  # indexes of the boxes that were already put in a bin
        alreadyUsed = 0  # sees if the current box was already placed in a box
        i = 0

        # goes through every box to fit it into a bin
        while i < len(boxArr):
            # makes sure the current box has not already been used
            for x in range(len(fitted)):
                if i == fitted[x]:
                    alreadyUsed = 1
                    break
            if alreadyUsed != 1:
                j = i
                # goes through the rest of the boxes to see if any can fit
                while j < len(boxArr):
                    x = self.currBin
                    y = self.binArr
                    aBox = boxArr[j]  # current box

                    # check if the current box has already been placed
                    check = 0
                    for x in range(len(fitted)):
                        if j == fitted[x]:
                            check = 1
                            j += 1
                            break

                    # if the box was placed then no need to check if it will fit
                    if check == 1:
                        continue

                    # if the box has not been used then try to fit it
                    elif aBox[0] <= self.length and aBox[1] <= self.width and aBox[2] <= self.height:
                        # subtracts the current dimension available from the dimensions
                        # of the current box you are trying to fit
                        newSide1 = newSide1 - aBox[0]
                        newSide2 = newSide2 - aBox[1]
                        newSide3 = newSide3 - aBox[2]

                        # adds the box to the volume to see if it can initially fit
                        totalVolume = totalVolume + aBox[0] * aBox[1] * aBox[2]

                        # checks if the box can fit focused on the largest dimension
                        if newSide1 >= 0 and newSide3 > 0 and totalVolume <= self.volume:
                            fitted.append(j)  # add index to show the box was used
                            self.currBin.append(aBox)  # add box to current bin
                            # reset the sides not focused on
                            newSide2 = newSide2 + aBox[1]
                            newSide3 = newSide3 + aBox[2]

                        # checks if the box can fit focused on the middle dimension, also making sure
                        # that when the box added will be able to fit by limiting the volume to 3/4
                        elif newSide2 >= 0 and newSide3 > 0 and totalVolume <= self.volume * 3 / 4:
                            fitted.append(j)  # add index to show the box was used
                            self.currBin.append(aBox)  # add box to current bin
                            newSide1 = newSide1 + aBox[0]
                            newSide3 = newSide3 + aBox[2]

                        # checks if the box can fit focused on the smallest dimension, also making sure
                        # that when the box added will be able to fit by limiting the volume to 3/4
                        elif newSide3 >= 0 and totalVolume <= self.volume * 3 / 4:
                            fitted.append(j)  # add index to show the box was used
                            self.currBin.append(aBox)  # add box to current bin
                            # reset the sides not focused on
                            newSide1 = newSide1 + aBox[0]
                            newSide2 = newSide2 + aBox[1]

                        # if the box can not fit reset the volumes and the sides so that it
                        # does not reflect putting the current box in
                        else:
                            totalVolume = totalVolume - aBox[0] * aBox[1] * aBox[2]
                            newSide1 = newSide1 + aBox[0]
                            newSide2 = newSide2 + aBox[1]
                            newSide3 = newSide3 + aBox[2]

                    j += 1  # next box

                    # if there is no room left in the bin, just break the loop to start a new container
                    if newSide1 < 0 and newSide2 < 0 and newSide3 < 0:
                        break

                # add the bin to the array that holds all the bins and their boxes
                # do this because you went through all the boxes, and they could not fit
                self.binArr.append(self.currBin)
                self.currBin = []  # reset the current bin

                totalVolume = 0  # reset volume
                # reset all the dimensions of the bin
                newSide1 = self.length
                newSide2 = self.width
                newSide3 = self.height

            alreadyUsed = 0  # resets that the current box was used
            i += 1  # next box

        # add the last bin to the list if needed
        if self.currBin:
            self.binArr.append(self.currBin)

        # print out each
        print("You need " + str(len(self.binArr)) + " bins to fit the boxes")
        for i in range(len(self.binArr)):
            print(self.binArr[i])


class Boxes:
    def __init__(self):
        self.theBoxes = []
        self.totalVolume = 0

    def addBoxes(self, l, w, h, count):
        l, w, h = fixOrder(l, w, h)  # makes the largest dimension l, second w, and third h
        volume = l * w * h
        self.totalVolume = volume * count + self.totalVolume  # only used to check the volume
        # add each box to an array
        for i in range(count):
            self.theBoxes.append([l, w, h])


def packingAlgorithm1():
    theBins = Bin(12, 9, 6)
    b = Boxes()
    b.addBoxes(5, 4, 3, 2)
    b.addBoxes(3, 3, 3, 6)
    b.addBoxes(6, 2, 2, 2)
    theBins.pack(b.theBoxes)

    theBins2 = Bin(12, 9, 6)
    b2 = Boxes()
    b2.addBoxes(5, 4, 3, 5)
    b2.addBoxes(3, 3, 3, 10)
    b2.addBoxes(6, 2, 2, 5)

    theBins2.pack(b2.theBoxes)

    theBins3 = Bin(12, 9, 6)
    b3 = Boxes()
    b3.addBoxes(5, 4, 3, 12)
    b3.addBoxes(3, 3, 3, 12)
    b3.addBoxes(6, 2, 2, 6)

    theBins3.pack(b3.theBoxes)


def packingAlgorithm2():
    theBins = Bin(12, 9, 6)
    b = Boxes()
    b.addBoxes(5, 4, 3, 2)
    b.addBoxes(3, 3, 3, 6)
    b.addBoxes(6, 2, 2, 2)
    theBins.pack2(b.theBoxes)

    theBins2 = Bin(12, 9, 6)
    b2 = Boxes()
    b2.addBoxes(5, 4, 3, 5)
    b2.addBoxes(3, 3, 3, 10)
    b2.addBoxes(6, 2, 2, 5)

    theBins2.pack2(b2.theBoxes)

    theBins3 = Bin(12, 9, 6)
    b3 = Boxes()
    b3.addBoxes(5, 4, 3, 12)
    b3.addBoxes(3, 3, 3, 12)
    b3.addBoxes(6, 2, 2, 6)

    theBins3.pack2(b3.theBoxes)


def packingAlgorithm3():
    theBins = Bin(12, 9, 6)
    b = Boxes()
    b.addBoxes(5, 4, 3, 2)
    b.addBoxes(3, 3, 3, 6)
    b.addBoxes(6, 2, 2, 2)
    theBins.pack3(b.theBoxes)

    theBins2 = Bin(12, 9, 6)
    b2 = Boxes()
    b2.addBoxes(5, 4, 3, 5)
    b2.addBoxes(3, 3, 3, 10)
    b2.addBoxes(6, 2, 2, 5)

    theBins2.pack3(b2.theBoxes)

    theBins3 = Bin(12, 9, 7)
    b3 = Boxes()
    b3.addBoxes(5, 4, 3, 12)
    b3.addBoxes(3, 3, 3, 12)
    b3.addBoxes(6, 2, 2, 6)

    theBins3.pack3(b3.theBoxes)


print("Algorithm 1 - The Most Bins on Average: ")
print(timeit.timeit('packingAlgorithm1()', setup='from __main__ import packingAlgorithm1', number=1))
print("\n \n")
print("Algorithm 2 - The Middle Amount Bins on Average: ")
print(timeit.timeit('packingAlgorithm2()', setup='from __main__ import packingAlgorithm2', number=1))
print("\n \n")
print("Algorithm 3 - The Least Bins on Average: ")
print(timeit.timeit('packingAlgorithm3()', setup='from __main__ import packingAlgorithm3', number=1))
# Package bin container is 12" x 9" x 6" box . It should be able to include 3 types of cubic items:
# 5" x 4" x 3"
# 3" x 3" x 3"
# 6" x 2" x 2"
# There are 3 level:
# 10 items: a: 2, b: 6, c: 2
# 20 items: a: 5, b: 10: c: 5
# 30 items: a: 12: b: 12: c: 6
