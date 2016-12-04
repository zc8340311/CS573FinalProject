import web
from collections import deque
import numpy as np
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.manifold import TSNE
urls = (
    '/index.html', 'index',
    '/try.html','try1',
    '/project.csv','projection_response',
    "/pca_data.csv","project_data",
    "/student-mat-readable.csv","response_data",
    "/parallel.html","parallel",
    "/parallel_1.html","parallel1",
    # "/stylesheets/d3.slider.css","css",
    # "/javascripts/d3.slider.js","js"
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
class css():
    def GET(self):
        with open(r"./stylesheets/d3.slider.css") as f:
            return f.read()
class js():
    def GET(self):
        with open(r"./javascripts/d3.slider.js") as f:
            return f.read()
class parallel():
    def GET(self):
        with open(r"parallel.html") as f:
            return f.read()
class parallel1():
    def GET(self):
        with open(r"parallel_1.html") as f:
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

        if web.input()["method"]=="pca":
            project_data = self.pca(X)
        if web.input()["method"]=="lda":
            project_data = self.lda(X)
        if web.input()["method"]=="tsne":
            project_data = self.tsne(X)
        
        print web.input()["color"]
        if web.input()["color"]=="trend":
            project_data = np.concatenate((project_data,y[:,0].reshape(y[:,0].size,1)),axis=1)
        else:
            project_data = np.concatenate((project_data,y[:,2].reshape(y[:,2].size,1)),axis=1)
        return self.to_csvString(head,project_data)
    def split(self,data):
        return data[:,0:33],data[:,-4:-1]
    def to_nparray(self,data):
        lines = deque(data.strip().split('\n'))
        head = lines.popleft().split(',')
        data = np.array([i.split(',') for i in list(lines)],dtype=np.float32)
        return head,data
    def pca(self,data):
        p = PCA()
        project_d = p.fit_transform(data)
        return project_d
    def lda(self,data):
        lda = LDA(n_components=2)
        fea = data.shape[1]
        X_r2 = lda.fit(data[:,0:fea-1], data[:,-1]).transform(data[:,0:fea-1])
        return X_r2
    def tsne(self,data):
        tsne = TSNE()
        project_d = tsne.fit_transform(data)
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
