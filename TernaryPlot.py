# -*- coding: utf-8 -*-
"""
@author: Bismarck Gomes Souza Junior
@email:  bismarckjunior@outlook.com
"""
from __future__ import division
from scipy import interpolate
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


class TernaryAxis():
    def __init__(self, fig, type_='bottom'):
        self.type = type_
        if type_ == 'right':
            self.beg = (1, 0)
            self.end = (0.5, 0.5*np.sqrt(3))
            self.phi_tick = np.pi
            self.transform_tick_label = (0.01, -0.004)
            self.transform_label = (0.1, 0.03)
            self.label_rotation = -60
            self.ha_tick_label = 'left'
        elif type_ == 'left':
            self.beg = (0.5, 0.5*np.sqrt(3))
            self.end = (0, 0)
            self.phi_tick = -np.pi/3
            self.transform_tick_label = (-0.01, -0.004)
            self.transform_label = (-0.1, 0.03)
            self.label_rotation = 60
            self.ha_tick_label = 'right'
        else:
            self.beg = (0, 0)
            self.end = (1, 0)
            self.phi_tick = np.pi/3
            self.transform_tick_label = (0, -0.04)
            self.transform_label = (0, -0.07)
            self.label_rotation = 0
            self.ha_tick_label = 'center'

        #Initializing variables
        self.percentage = False
        self.gridOn = True
        self.inverseOn = False
        self.min_max = True   # plots 0.0 and 1.0

        #Creating axis
        self.ax = ax = fig.add_subplot(111, aspect='equal')
        ax.set_xticks(())
        ax.set_yticks(())
        ax.set_frame_on(False) 
        self.text = ax.text
        self.plots = {'ticks':[], 'ticks_label':[], 'grids':[], 'label':[], 'inverse':[]}
        self.set_ticks()
    
    def cla(self):
        '''Clears axis.'''
        self.remove('ticks')
        self.remove('ticks_label')
        self.remove('label')
        self.remove('grids') 
        self.remove('inverse')
    
    def remove(self, plot):
        '''Removes the plot. plot=[ticks, labels, grids, label].'''
        if plot in self.plots and self.plots[plot]:
            for p in self.plots[plot]:
                try:
                    p.pop(0).remove()
                except:
                    try: p.remove()
                    except: pass
            self.plots[plot] = []
            return True
        else:
            return False
    
    def set_label(self, text, **kw):
        '''Sets the axis label.'''
        self.remove('label')   
        xy = (np.array(self.beg)+np.array(self.end))/2.+np.array(self.transform_label)
        if self.label_rotation:
            self.plots['label'] = [self.text(xy[0],xy[1], text, ha='center', va='center', rotation=self.label_rotation, **kw)]
        else:
            self.plots['label'] = [self.text(xy[0],xy[1], text, ha='center', va='top', **kw)]
    
    def get_label(self):
        '''Gets the label.'''
        return self.plots['label'][0].get_text() if self.plots['label'] else ''        
        
    def set_ticks(self, ticks=10, llen_ticks=0.01, lw_ticks=1.2):
        '''Sets ticks. 
        ticks: list or integer
        llen_ticks: line lenght
        lw_ticks: line width
        ''' 
        self.ticks = []
        self.labels = []
        try:  
            ticks = [i/ticks for i in range(ticks+1)]
        except: 
            ticks = list(ticks)
            ticks.sort()
        for tick in ticks:
            xy = np.array(self.beg) + tick*(np.array(self.end)-np.array(self.beg))
            self.ticks.append(tuple(xy))
            self.labels.append(tick)
        self.llen_ticks=llen_ticks
        self.lw_ticks = lw_ticks
        self.update()
   
    def grid(self, toggle=None, grid_ticks=None, **kw):
        '''Removes or plots the grids.'''
        #Removing grids
        self.remove('grids')
        self.gridOn = False
        if not(toggle==None and self.gridOn or not toggle):
            #Ploting grids
            self.gridOn = True
            self.grid_ticks = grid_ticks if grid_ticks else self.ticks
            if 'linestyle' not in kw: kw['linestyle'] = ':'
            if 'color' not in kw: kw['color'] = 'k'
            if 'lw' not in kw: kw['lw'] = '.5'
            for tick in self.grid_ticks:
                x1,y1 = tuple(tick)
                x2,y2 = self.__boundary_point(tick)
                plt_grid = self.ax.plot([x1,x2],[y1,y2], **kw)
                self.plots['grids'].append(plt_grid)
    
    def remove_ticks_label(self):
        '''Removes ticks label.'''
        self.remove('ticks_label')
        if self.type=='right':
            transform = (0.035,0.02)
        elif self.type=='left':
            transform = (-0.035,0.02)
        else:
            transform = (0,-0.03)
        xy = (np.array(self.beg)+np.array(self.end))/2.+np.array(transform)
        if 'label' in self.plots and self.plots['label']:
            text = self.plots['label'][0].get_text()
            fp= self.plots['label'][0].get_font_properties()
            self.remove('label')
            if self.label_rotation:
                self.plots['label'] = [self.text(xy[0],xy[1], text, ha='center', va='center', rotation=self.label_rotation)]
            else:
                self.plots['label'] = [self.text(xy[0],xy[1], text, ha='center', va='top')]
            self.plots['label'][0].set_font_properties(fp)
        
    def __inverse(self):
        '''Changes the tick angle.'''
        self.inverseOn = not self.inverseOn
        if self.type == 'right':
            self.phi_tick = -2*np.pi/3 if self.inverseOn else np.pi
        elif self.type == 'left':
            self.phi_tick = 0 if self.inverseOn else -np.pi/3
        else:
            self.phi_tick = 2*np.pi/3 if self.inverseOn else np.pi/3
                    
    def inverse(self):
        '''Inverse the axis.'''
        self.__inverse()
        self.update()
    
    def plot_inverse_ticks(self):
        '''Plots the invese ticks.'''
        self.__inverse()
        self.__plot_ticks()
        self.__inverse()
                
    def update(self):
        '''Updates the graph.'''
        self.remove('ticks')
        self.remove('ticks_label')
        self.remove('grids') 
        self.__plot_ticks()
        self.__plot_ticks_label()
        if self.gridOn: self.grid(True)        
   
    def __rect(self, r, phi):
        '''From polar coordinates to rectangle coordinates.'''
        return (r*np.cos(phi), r*np.sin(phi))
    
    def __plot_ticks(self):
        '''Plots the ticks. llen_ticks: line lenght. lw_ticks: line width'''
        for tick in self.ticks:
            if tick not in [(0,0),(1,0)] and (tick[0]!=0.5 or tick[1]==0): 
                x1,y1 = tuple(tick)
                x2,y2 = tuple(np.array(tick)+np.array(self.__rect(self.llen_ticks, self.phi_tick))) 
                plt_tick = self.ax.plot([x1,x2], [y1,y2], 'k-', lw=self.lw_ticks)
                self.plots['ticks'].append(plt_tick)
    
    def __plot_ticks_label(self):
        '''Plots the ticks label.'''
        for tick, label in zip(self.ticks, self.labels[::1-2*int(self.inverseOn)]):
            if not self.min_max:
                if tick in [(0,0),(1,0)] or tick[0]==0.5 and tick[1]!=0:
                    continue 
            xy_label = np.array(tick)+np.array(self.transform_tick_label)
            if self.percentage: label = '%g%%' % (label*100)
            plt_labels = self.text(xy_label[0], xy_label[1], label, ha=self.ha_tick_label, fontsize=11)
            
            self.plots['ticks_label'].append(plt_labels)
             
    def __boundary_point(self, xy):
        '''Finds the triangle boundary.'''
        x, y = tuple(xy)
        if x+y==0 or x+y==1:  return xy
        tan = np.tan(self.phi_tick)
        tan1 = np.tan(0)
        tan2 = np.tan(np.pi/3)
        tan3 = np.tan(2*np.pi/3)
        
        #Intersection with bottom line
        x1 = (y-tan*x)/(tan1-tan) if tan1!=tan else 2
        y1 = 0
       
        #Intersection with left line
        x2 = (y-tan*x)/(tan2-tan) if tan2!=tan else 2
        y2 = x2*tan2
        
        #Intersection with right line
        x3 = (-y+tan*x-tan3)/(tan-tan3)  if tan3!=tan else 2
        y3 = (x3-1)*tan3
        
        for a,b in [(x1,y1),(x2,y2),(x3,y3)]:
            if not (abs(a-x)<1E-3 and abs(b-y)<1E-3 ) and 0<=a<=1 and 0<=b<=1:
                return (a,b)                
        return (a,b)
    
        
class PyTernary():
    def __init__(self, fig, title='', main_labels=[], short_labels=[],
                 canvas=plt):
        #Setting figure
        self.fig = fig

        #Clearing plot
        self.clear_plot()

        #Setting canvas
        self.canvas = canvas

        #Initializing some variables
        self.inverseOn = False
        self.min_maxOn = True
        self.gridOn = True
        self.plots = {'plots': [], 'templates': [], 'short_labels': []}

        #Setting and ploting title and labels
        self.title = title
        self.main_labels = main_labels
        self.short_labels = short_labels
        if title: self.set_title(title, fontsize=21)
        if main_labels: self.set_main_labels(main_labels, fontsize=13)
        if short_labels: 
            self.set_short_labels(short_labels, d=0.98, fontsize=16)
            self.show_min_max(False)     
        
    def set_title(self, title, **kw):
        '''Sets title.'''
        self.__ax.set_title(title, **kw)
    
    def set_main_labels(self, labels, **kw):
        '''Sets main labels.'''
        for i,ax in enumerate(self.axes):
            ax.set_label(labels[i], **kw)
            
    def set_short_labels(self, labels, d=0.98, **kw):
        '''Sets the label on the  edges of the triangle.'''
        if self.min_maxOn:
            locations = [(0.5,0.91), (-0.06,-0.03), (1.06,-0.03)]
        else:
            locations = [(0.5,0.89), (-0.025,-0.03), (1.025,-0.03)]
        has = ['center', 'right', 'left']
        vas = ['bottom', 'center', 'center']
        if hasattr(self, 'short_title'):
            for i in range(3): self.plots['short_labels'].pop().remove()
        else:
            self.short_title = []
        self.d_title(d)
        
        if not 'fontsize' in kw:
            kw['fontsize'] = 16
            
        for i,xy in enumerate(locations):
            short_label = self.__ax.text(xy[0], xy[1], labels[i], ha=has[i], va=vas[i], **kw)
            self.plots['short_labels'].append(short_label)
    
    def transform_points(self, data):
        '''Transforms from x1,x2,x3 to x,y data and from x,y to x1,x2,x3 data.'''
        try: len(data[0])
        except: data = [data]
        
        if data and len(data[0])==3:
            data = np.matrix([[d/sum(row) for d in row] for row in data], np.float64)
            A = np.matrix([[.5,.5*np.sqrt(3)],[0,0],[1,0]])
            xy = np.array(data*A)
            return xy[:,0], xy[:,1]
        elif data and len(data[0])==2:
            data = np.matrix(data)
            A = np.matrix([[0,-np.sqrt(3),np.sqrt(3)],[2.,-1,-1]])/np.sqrt(3)
            B = np.matrix([[0,1,0]]*len(data))
            xyz = np.array(data*A+B)
            return xyz[:,0], xyz[:,1], xyz[:,2]
    
    def __plot_data(self, data, **kw):
        '''Plots data with the same settings.'''
        x, y = self.transform_points(data)
        if 'marker' not in kw:
            kw['linestyle'] = ''
            kw['marker'] = 'o'
        return self.ax.plot(x, y, **kw)
        
    def plot_data(self, data, **kw):
        '''Plots data with the same settings and return the index.'''
        plot = self.__plot_data(data, **kw)
        self.plots['plots'].append(plot)
        index = len(self.plots['plots'])-1
        return index

    def add_null_plot(self):
        '''Adds null plot.'''
        self.plot['plots'].append([])
  
    def update_plot(self, index, data=None, **kw):
        '''Updates data plot.'''
        if data:
            try:
                self.plots['plots'][index][0].remove()
            except:
                pass
            xy = self.transform_points(data)
            if xy:
                self.plots['plots'][index] = self.ax.plot(xy[0], xy[1], **kw)
            else:
                self.plots['plots'][index] = []
        else:
            self.plots['plots'][index][0].update(kw)
        if hasattr(self, 'legend_labels'):
            self.legend(self.legend_labels)
        self.draw()

    def legend(self, labels):
        '''Plots the legend.'''
        n = len(labels) if len(labels)<13 else 13  
        self.legend_labels = labels
        lines, labels_ = [], []
        for line, label in zip(self.plots['plots'], labels):
            if line:
                lines.append(line[0])
                labels_.append(label)
        self.plots['legend'] = self.ax.legend(lines, labels_, loc=2, 
                       numpoints=1, bbox_to_anchor=(0.70+0.03*n, .2, 1.2, 0.75))
        
    def grid(self, toggle=None, **kw):
        '''Plots or removes the grids.'''
        for ax in self.axes:
            ax.grid(toggle, **kw)
        self.gridOn = ax.gridOn
            
    def percentage(self, toggle=None):
        '''Changes to percentage.'''
        for ax in self.axes:
            ax.percentage = toggle if toggle else not ax.percentage
            ax.update()
    
    def inverse(self):
        '''Inverses the axes.'''
        A,B,C = tuple(self.get_main_labels())
        new_labels = [B,C,A] if self.inverseOn else [C,A,B]
        self.inverseOn = not self.inverseOn
        for ax,t in zip(self.axes, new_labels):
            ax.inverse()
            ax.set_label(t)
    
    def __plot_template(self, data, kind, **kw):
        '''Plots the template using linear or cubic interpolation.''' 
        data.sort(key=lambda xyz:xyz[-1]/float(sum(xyz)))
        x, y = self.transform_points(data)
        if kind=='fill':
            if 'fill' not in kw: kw['fill']=False
            #hatch=['/' | '\' | '|' | '-' | '+' | 'x' | 'o' | 'O' | '.' | '*' ]
            template = self.ax.fill(x, y, **kw)
        else:
            if 'linestyle' not in kw: kw['linestyle'] = '-'
            if 'color' not in kw: kw['color'] = 'k'
            if 'lw' not in kw: kw['lw'] = 1.2
            if kind=='linear':
                template = self.ax.plot(x, y, **kw)
            elif kind=='cubic':
                f = interpolate.interp1d(x, y, kind)  
                x_ = np.linspace(min(x), max(x), 50)
                template = self.ax.plot(x_, f(x_), **kw)
        return template
        
    def plot_template(self, data, kind='linear', **kw):
        '''Plots the template using linear or cubic interpolation and return 
        index.''' 
        template = self.__plot_template(data, kind, **kw)
        self.plots['templates'].append(template)
        index = len(self.plots['templates'])-1
        return index
        
    def get_main_labels(self):
        '''Gets main labels.'''
        return [ax.get_label() for ax in self.axes]
        
    def show_min_max(self, toggle=None):
        '''Toggles between showing the minimum and maximum values or not.'''
        self.min_maxOn = toggle if toggle else not self.min_maxOn
        for ax in self.axes:
            ax.min_max = self.min_maxOn
            ax.update()
        if self.short_labels:
            fs = self.plots['short_labels'][0].get_fontsize()
            self.set_short_labels(self.short_labels, d=0.98, fontsize=fs)
            
    def clear_plot(self, index = None):
        '''Clears the plot.'''
        if index:
            try:
                self.plots['plots'][index][0].remove()
                self.plots['plots'][index] = []
            except:
                pass
        else:
            #Clearing figure
            self.fig.clf()
            
            #Clearing axes
            ax = self.fig.add_subplot(111, aspect='equal')
            ax.set_ylim(-0.01, 0.92)
            ax.set_xlim(-0, 1.01)
            self.d_title = lambda d: ax.set_ylim(-0.01, d)
            
            #Creating background
            p = patches.Polygon([(0,0),(0.5,0.5*np.sqrt(3)),(1,0),(0,0)], 
                                 facecolor="white",edgecolor="black", lw=1.)
            ax.add_patch(p)
            
            #Setting main axis
            self.__ax = ax
            self.ax = self.fig.add_subplot(111, aspect='equal')
            
            #Creating axes
            self.__create_axes()  
    
    def show(self):
        '''Shows the graphic.'''
        self.canvas.show()    
    
    def draw(self):
        '''Draws the graphic.'''
        self.canvas.draw()
        
    def __create_axes(self):
        '''Creates the axes.'''
        self.axRight = TernaryAxis(self.fig, 'right')
        self.axLeft = TernaryAxis(self.fig, 'left')
        self.axBottom = TernaryAxis(self.fig, 'bottom')
        self.axes = [self.axRight, self.axLeft, self.axBottom]
        
if __name__=='__main__':
    fig = plt.figure()       
    T = PyTernary(fig, 'Ternary Plot', ['Big A', 'Big B', 'Big C'], ['A','B','C'])
    data = [ [10,20,70], [20,25,55], [0.5,0.2,0.3]]
    T.plot_data(data, color='green')
    T.plot_data([[60,10,30],[25,5,70]])
    T.plot_template(data+[[40,50,10]],'fill', hatch='/', fill=False, edgecolor='k', color='c')
    T.legend(['Sample 1', 'Sample 2'])
    #TP.inverse()
    #TP.update_plot(1, [[]], color='k', markersize=10, marker='o')
    T.show()

    