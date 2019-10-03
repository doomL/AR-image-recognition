from abc import ABC, abstractmethod

class AlgorithmChooser(ABC):

    @abstractmethod
    def doAlgorithm(self):
        pass


class SiftAlgorithm(AlgorithmChooser):
    def doAlgorithm(self, img):
        frame = np.asarray(img)
        keypointsFrame, descriptorsFrame = detector.detectAndCompute(
            frame, None)

        for index in range(len(loader.imgArray)):
            knn_matchesFrame = matcher.knnMatch(
                descriptorsArr[index], descriptorsFrame, 2)

            for m, n in knn_matchesFrame:
                if m.distance < ratio_tresh * n.distance:
                    good_matches.append(m)

        if good_matches != None and len(good_matches) >= MIN_MATCHES:
            print("Banconota ", index)

        good_matches.clear()

        return img


class SurfAlgorithm(AlgorithmChooser):
    def doAlgorithm(self, img):
        frame = np.asarray(img)
        keypointsFrame, descriptorsFrame = detector.detectAndCompute(
            frame, None)

        for index in range(len(loader.imgArray)):
            knn_matchesFrame = matcher.knnMatch(
                descriptorsArr[index], descriptorsFrame, 2)

            for m, n in knn_matchesFrame:
                if m.distance < ratio_tresh * n.distance:
                    good_matches.append(m)

        if good_matches != None and len(good_matches) >= MIN_MATCHES:
            print("Banconota ", index)

        good_matches.clear()

        return img
