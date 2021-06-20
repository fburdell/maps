import shapefile as shp  # Requires the pyshp package
import matplotlib.pyplot as plt; from descartes import PolygonPatch
import os
from Polygon import Polygon #paths 

house_path =      r"shapes/tl_2017_42_sldl"
senate_path =       r'shapes/FinalSenatePlan2012'

class Colors: 

    def __init__(self): 
        self.white = '#ffffff'
        self.black = '#000000'
        self.red = '#ff0000'
        self.navy = '#004299'

        self.salmon = '#ffabab' #GOP CAUCUS
        self.cornflower = '#abcfff' #DEM CAUCUS
        self.pastel_yellow = '#FFE5AD'
        self.pastel_green = '#BAFFAD'
        self.pastel_purple = '#ADB8FF'
        self.pastel_pink = '#FFADEA'
        self.pastel_aqua = '#ADFFF8'

class Geos: 


    def __init__(self): 
        import pandas as pd
        rf = pd.read_csv(r'inputs/regionals.csv')

        self.protect = [55,72,50,143,119,53,9,165,162,146]
        self.tier = [105,168,30,151,29,178,44,152,18,160,26,144,28,106,120]
        self.emerge = [147,176,87,131,48,104,97,171,138]
        self.cate = list(rf[rf.person == 'Cate Peterson'].hd.values)
        self.dylan = list(rf[rf.person == 'Dylan Doody'].hd.values)
        self.sawyer = list(rf[rf.person == 'Sawyer Neale'].hd.values)
        self.megan = list(rf[rf.person == 'Megan Lafayette'].hd.values)
        self.kali = list(rf[rf.person == 'Kali Cummings'].hd.values)
        self.dgfb = list(rf[rf.person == 'DGFB'].hd.values)
        self.catekali = list(rf[rf.person == 'CateKali'].hd.values)


class Fshp: 

    import shapefile as shp  # Requires the pyshp package
    from Polygon import Polygon
    import pandas as pd 

    
    #place direct in to mapping env for now...
    #fa.ax.axis('scaled')


    def __init__(self, path): 
        from simpledbf import Dbf5
        import matplotlib.pyplot as plt

        self.shape = path+".shp"
        self.dbf = path+".dbf"
        self.db = Dbf5(self.dbf)
        self.df = self.db.to_dataframe()
        self.fshp = shp.Reader(self.shape,self.dbf)
        self.fig = plt.figure()
        self.ax = self.fig.gca()

        plt.axis('off')
        plt.legend()

        self.ax.axis('scaled')

    def __len__(self): 
        return len(self.fshp)

    def __iter__(self): 
        for r in self.fshp.iterShapes():
            yield r #shapefile.shape object

    def set_mpatches(self, dikt): 
        import matplotlib.patches as mpatches
        li = list()
        for k, v in dikt.items(): 
             li.append(mpatches.Patch(color=k,label=v))
        return li

    def set_title(self, title): 
        return plt.title(title)

    def set_legend(self, dikt, title): 
        import matplotlib.patches as mpatches
        """
        expecting dikt of handles:labels
        eg: 
        dikt = {c.pastel_yellow :   'Dylan Doody',
                c.pastel_green  :   'Sawyer Neale',
                c.pastel_purple :   'Cate Peterson',
                c.pastel_pink   :   'Kali Cummings',
                c.cornflower    :   'Megan Lafayette',
                c.pastel_aqua   :   'Dena Gleason &\n Frank Burdell'}
        """

        plt.legend(handles=self.set_mpatches(dikt), 
                title=title, 
                fontsize='xx-small',
                loc=9,
                bbox_to_anchor=(.21,-.25,.25,.25),
                ncol=3,
                frameon=True)


    def apply(self,f): 
        return self.df.apply(f, axis=0)

    def save(self, path): 
        self.ax.axis('scaled')
        self.fig.savefig(path, dpi=300)

    def show(self): 
        self.ax.axis('scaled')
        plt.show()



def shape_center(shape):
	"""
	computes the center of gravity of a shapefile multi-polygon
	shape must be an instance of shapefile._Shape of the Python Shapefile Library
	http://packages.python.org/Python%20Shapefile%20Library/
	Polygon class comes from here
	http://pypi.python.org/pypi/Polygon/1.17
	"""
	from Polygon import Polygon
	parts = shape.parts[:]
	parts.append(len(shape.points))
	
	# the center computation produces false results for 
	# countries whose shapes cross the 180° longitude
	# we need to check this
	far_east = False
	far_west = False
	for i in range(len(parts)-1):
		pts = shape.points[parts[i]:parts[i+1]]
		if len(pts) == 0: continue
		if pts[0][0] < -90:
			far_west = True
		if pts[0][0] > 90:
			far_east = True
	
	# now we convert the Shape into a Polygon
	poly = Polygon()
	for i in range(len(parts)-1):
		pts = shape.points[parts[i]:parts[i+1]]
		if far_east and far_west:
			# correct points if country crosses 180° lon
			for j in range(len(pts)):
				if pts[j][0] < 0: pts[j][0] += 360
		poly.addContour(pts)
	# and return its center of gravity
	return poly.center()


t = Geos()
c = Colors()
fa = Fshp(house_path)


def map():
    for i, r in enumerate(fa): 
        i+=1
        print(i)

        if i in t.dylan: 
            fa.ax.add_patch(PolygonPatch(r, ec=c.black, fc=c.pastel_yellow, linewidth=.1, label='Dylan'))
        elif i in t.sawyer: 
            fa.ax.add_patch(PolygonPatch(r, ec=c.black, fc=c.pastel_green, linewidth=.1))
        elif i in t.cate: 
            fa.ax.add_patch(PolygonPatch(r, ec=c.black, fc=c.pastel_purple, linewidth=.1))
        elif i in t.kali: 
            fa.ax.add_patch(PolygonPatch(r, ec=c.black, fc=c.pastel_pink, linewidth=.1))
        elif i in t.megan: 
            fa.ax.add_patch(PolygonPatch(r, ec=c.black, fc=c.cornflower, linewidth=.1))
        elif i in t.dgfb: 
            fa.ax.add_patch(PolygonPatch(r, ec=c.black, fc=c.pastel_aqua, linewidth=.1))
        elif i in t.catekali: 
            fa.ax.add_patch(PolygonPatch(r, ec=c.black, fc=c.white, linewidth=.1))
        else: 
            fa.ax.add_patch(PolygonPatch(r, ec=c.black, fc=c.white, linewidth=.1))

    dikt = {c.pastel_yellow :   'Dylan Doody',
            c.pastel_green  :   'Sawyer Neale',
            c.pastel_purple :   'Cate Peterson',
            c.pastel_pink   :   'Kali Cummings',
            c.cornflower    :   'Megan Lafayette',
            c.pastel_aqua   :   'Dena Gleason &\n Frank Burdell'}

    fa.set_legend(dikt, 'Key')
    fa.save(r'outputs/regionals.png')
    fa.show()

map()

