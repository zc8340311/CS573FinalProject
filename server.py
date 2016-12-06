import web
from collections import deque
import numpy as np
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.manifold import TSNE
from sklearn.manifold import MDS
from sklearn.manifold import Isomap
urls = (
    '/index.html', 'index',
    '/try.html','try1',
    '/project.csv','projection_response',
    "/pca_data.csv","project_data",
    "/student-mat-readable.csv","response_data",
    "/parallel.html","parallel",
    "/parallel_1.html","parallel1",
    "/parallel_3.html","parallel_3",
    "/parallel_4.html","parallel_4"
)
app = web.application(urls, globals())

class index:
    def GET(self):
		with open(r"index.html",'r') as f:
			return f.read()

class try1():
    def GET(self):
        with open(r"try.html") as f:
            return f.read()

class parallel():
    def GET(self):
        with open(r"parallel.html") as f:
            return f.read()
class parallel1():
    def GET(self):
        with open(r"parallel_1.html") as f:
            return f.read()

class parallel_3():
    def GET(self):
        with open(r"parallel_3.html") as f:
            return f.read()
class parallel_4():
    def GET(self):
        with open(r"parallel_4.html") as f:
            return f.read()
class response_data():
    def GET(self):
        print "data",web.input()
        with open(r"./data/student-mat-readable.csv") as f:
            return f.read()
class project_data():
    def GET(self):
        print "pca data",web.input()
        print "pca url"
        with open(r"./data/clean_student_mat.csv") as f:
            head,data = self.to_nparray(f.read())
        head = ["d1","d2","color"]
        X,y = self.split(data)
        X = self.feature_emph( X, web.input()["features"])
        if web.input()["method"]=="pca":
            project_data = self.pca(X)
        if web.input()["method"]=="lda":
            project_data = self.lda(X,y[:,0])
        if web.input()["method"]=="tsne":
            project_data = self.tsne(X)
        if web.input()["method"]=="mds":
            project_data = self.mds(X)
        if web.input()["method"]=="isomap":
            project_data = self.mds(X)

        print "color",web.input()["color"]
        if web.input()["color"]=="trend":
            project_data = np.concatenate((project_data,y[:,1].reshape(y[:,1].size,1)),axis=1)
        elif web.input()["color"]=="give_up":
            project_data = np.concatenate((project_data,y[:,2].reshape(y[:,2].size,1)),axis=1)
        return self.to_csvString(head,project_data)
    def feature_emph(self,data,weight):
        weights = map(int,weight.split(","))
        feature_locations = [2, 6, 7, 8, 9, 10, 15, 27, 29]
        for w,location in zip(weights,feature_locations):
            data[:,location] = data[:,location] * w
        return data
    def split(self,data):
        return data[:,0:33],data[:,33:36]
    def to_nparray(self,data):
        lines = deque(data.strip().split('\n'))
        head = lines.popleft().split(',')
        data = np.array([i.split(',') for i in list(lines)],dtype=np.float32)
        return head,data
    def pca(self,data):
        p = PCA()
        project_d = p.fit_transform(data)
        return project_d
    def lda(self,data,y):
        lda = LDA(n_components=2)
        X_r2 = lda.fit(data, y).transform(data)
        return X_r2
    def tsne(self,data):
        tsne = TSNE()
        project_d = tsne.fit_transform(data)
        return project_d
    def mds(self,data):
        mds = MDS()
        project_d = mds.fit_transform(data)
        return project_d
    def isomap(self,data):
        isomap = Isomap()
        project_d = isomap.fit_transform(data)
        return project_d

    def fake_pca(self,data):
        u,c,v = np.linalg.svd(data,full_matrices=False)
        c[1] = 0
        data = np.dot(u,np.dot(np.diag(c),v))
        return data
    def to_csvString(self,head,data):
        data_to_text = [",".join(map(str,i)) for i in data]
        return "\n".join([",".join(head),"\n".join(data_to_text)])
if __name__ == "__main__":
    app.run()
