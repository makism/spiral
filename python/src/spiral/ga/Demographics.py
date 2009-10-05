"""

"""


try:
    from matplotlib.pyplot import *
    from matplotlib.colors import *
    from numpy import *
    
    HAS_REQUIRED_LIBS = True
except:
    HAS_REQUIRED_LIBS = False



class PopulationDemographics (object):
    
    def __init__ (self, Epochs=128, PopulationSize=64):
        self.totalMutations = 0
        self.totalGenomes   = Epochs * PopulationSize
        self.Population     = { }
            
    def register (self, Population):
        id = Population.Id
        
        if id not in self.Population.keys ():
            self.Population[id] = {
                "migrations":Population.Migrations,
                "mutations": Population.Mutations,
                "fit_avg"  : Population.Fitness.avg,
                "fit_max"  : Population.Fitness.max,
                "fit_min"  : Population.Fitness.min,
                "fit_total": Population.Fitness.total,
                "crossovers": Population.Crossovers,
                "cache_hits": Population.Fitness.hits,
                "cache_misses":Population.Fitness.misses
            }
        
            self.totalMutations += Population.Mutations
    
    def __len__ (self):
        return len(self.Population)
    
    def __getitem__ (self, item):
        return self.Population [item]
        
    def __setitem__ (self, index, value):
        self.Population [index] = value


class GenerationDemographics (object):
    
    def __init__ (self):
        pass
    
    
class Plotter (object):
    
    def __init__ (self, DemographicsObject, targetdir="/home/makism/Desktop/", prefix=None, x_step = 7, y_step=2):
        self.Demo = DemographicsObject
        
        self.target = targetdir
        self.prefix = prefix
        
        self.fitnessMax = self.Demo.Population[1]['fit_max']
        self.fitnessMin = self.Demo.Population[1]['fit_min']
        self.mutationsMax = self.Demo.Population[1]['mutations']
        self.mutationsMin = self.Demo.Population[1]['mutations']
        
        self.x_step = x_step
        self.y_step = y_step
        
        self.y_avg = list ()
        self.y_min = list ()
        self.y_max = list ()
        self.y_mut = list ()
        self.y_cross = list ()
        self.y_migra= list ()
        
        for i in self.Demo.Population:
            # migrations
            self.y_migra.append (self.Demo.Population[i]['migrations'])
            
            # crossovers
            self.y_cross.append (self.Demo.Population[i]['crossovers'])
            
            # mutations
            self.y_mut.append (self.Demo.Population[i]['mutations'])
            
            if self.Demo.Population[i]['mutations'] > self.mutationsMax:
                self.mutationsMax = self.Demo.Population[i]['mutations']
                
            if self.Demo.Population[i]['mutations'] < self.mutationsMin:
                self.mutationsMin = self.Demo.Population[i]['mutations']
            
            # fitness
            self.y_avg.append (self.Demo.Population[i]['fit_avg'])
            self.y_min.append (self.Demo.Population[i]['fit_min'])
            self.y_max.append (self.Demo.Population[i]['fit_max'])
            
            if self.Demo.Population[i]['fit_max'] > self.fitnessMax:
                self.fitnessMax = self.Demo.Population[i]['fit_max']
            
            if self.Demo.Population[i]['fit_min'] < self.fitnessMin:
                self.fitnessMin = self.Demo.Population[i]['fit_min']
                
    def plotMigration (self):
        if HAS_REQUIRED_LIBS:
            f = figure (figsize=(10, 7))
            
            title ('Successful Migrations Per Population')
            xlabel('Populations')
            ylabel('Total Migrands')
            
            y_migra = array (self.y_migra)
            
            #yticks ( range(self.mutationsMin, self.mutationsMax, self.y_step))
            xticks ( range(0, len(self.Demo), self.x_step) )
            
            plot (y_migra)
                        
            grid (color='gray')
            
            if self.prefix is not None:
                f.savefig ("%s/%s_migration.png" % (self.target, self.prefix))
            else:
                f.savefig ("%s/migration.png" % self.target)
                
    def plotCrossover (self):
        if HAS_REQUIRED_LIBS:
            f = figure (figsize=(10, 7))
            
            title ('Successful Crossovers Per Population')
            xlabel('Populations')
            ylabel('Total Crossovers')
            
            y_mut = array (self.y_mut)
            
            #yticks ( range(self.mutationsMin, self.mutationsMax, self.y_step))
            xticks ( range(0, len(self.Demo), self.x_step) )
            
            plot (y_mut)
                        
            grid (color='gray')
            
            if self.prefix is not None:
                f.savefig ("%s/%s_crossover.png" % (self.target, self.prefix))
            else:
                f.savefig ("%s/crossover.png" % self.target)
                
    def plotMutation (self):
        if HAS_REQUIRED_LIBS:
            f = figure (figsize=(10, 7))
            
            title ('Mutations Per Population')
            xlabel('Populations')
            ylabel('Mutations')
            
            y_mut = array (self.y_mut)
            
            yticks ( range(self.mutationsMin, self.mutationsMax, self.y_step))
            xticks ( range(0, len(self.Demo), self.x_step) )
            
            plot (y_mut)
                        
            grid (color='gray')
            
            if self.prefix is not None:
                f.savefig ("%s/%s_mutation.png" % (self.target, self.prefix))
            else:
                f.savefig ("%s/mutation.png" % self.target)
    
    
    def plotFitness (self):
        if HAS_REQUIRED_LIBS:
            f = figure (figsize=(10, 7))
            
            y_avg = array (self.y_avg)
            y_min = array (self.y_min)
            y_max = array (self.y_max)
            
            title ('Average,Max & Min Fitnesses')
            xlabel ('Populations')
            ylabel ('Fitness Score')
            
            #yticks ( range(self.fitnessMin-50, self.fitnessMax+50, self.y_step) )
            xticks ( range(0, len(self.Demo), self.x_step) )
            
            plot (y_avg, 'b-', label="avg")
            plot (y_min, 'r', label="min")
            plot (y_max, 'g', label="max")
            grid (color='gray')
            legend ()
            
            if self.prefix is not None:
                f.savefig ("%s/%s_fitness.png" % (self.target, self.prefix))
            else:
                f.savefig ("%s/fitness.png" % self.target)
  
  
class MultiPlotter (object):
    def __init__ (self, DemographicsObjects, targetdir="/home/makism/Desktop/", x_step = 7, y_step=2):
        
        self.Demos = DemographicsObjects        
        self.target = targetdir
         
        self.x_step = x_step
        self.y_step = y_step
        
        self.y_avg = dict ()
        self.y_min = dict ()
        self.y_max = dict ()
        
        self.y_cache_hits  = dict ()
        self.y_cache_misses= dict ()
        
        i = 0
        for demo in self.Demos:
            self.y_avg[i] = list () 
            self.y_max[i] = list ()
            self.y_min[i] = list ()
            #self.y_cache_hits[i]  = list ()
            #self.y_cache_misses[i]= list ()
            
            for x in demo.Population:
                self.y_avg[i].append (demo.Population[x]['fit_avg'])
                self.y_max[i].append (demo.Population[x]['fit_max'])
                self.y_min[i].append (demo.Population[x]['fit_min'])
                
                #self.y_cache_hits[i].append (demo.Population[x]['cache_hits'])
                #self.y_cache_misses[i].append (demo.Population[x]['cache_misses'])
                        
            i += 1
        
                
    def multiPlotFitness (self):
        if HAS_REQUIRED_LIBS:
            f = figure (figsize=(20, 14))
            
            title ('Average,Max & Min Fitnesses, Parallel=%d' % len(self.Demos))
            
            xlabel ('Populations')
            ylabel ('Fitness Score')
            
            colors = gradient ("ff0000", "0000ff", len(self.Demos))
            for i in self.y_avg:
                title ('Controller %d' % (i+1))
                subplot (2, 2, i+1)
                xticks ( range(0, 128, self.x_step) )
                y_avg = array (self.y_avg[i])
                plot (y_avg, color="#%s" % colors[i])
                grid (color='gray')
                #legend ()
            
            f.savefig ("%s/parallel_multifitness.png" % self.target)
            
                
    def plotFitness (self):
        if HAS_REQUIRED_LIBS:
            f = figure (figsize=(10, 7))
            
            title ('Parallel=2, Fitness Score')
            xlabel ('Epochs (one population per Epoch)')
            ylabel ('Fitness Score')
            
            xticks ( range(0, 128, self.x_step) )
            
            y_avg1 = array (self.y_avg[0])
            y_avg2 = array (self.y_avg[1])
            
            y_max1 = array (self.y_max[0])
            y_max2 = array (self.y_max[1])
            
            y_min1 = array (self.y_min[0])
            y_min2 = array (self.y_min[1])
            
            plot (y_avg1,"b", label="avg")
            plot (y_avg2, "b:")
            
            plot (y_max1,"g", label="max")
            plot (y_max2, "g:")
            
            plot (y_min1,"r", label="min")
            plot (y_min2, "r:")
            
            grid (color='gray')
            legend ()
            
            f.savefig ("%s/parallel_fitness.png" % self.target)
            
    def plotCache (self):
            f = figure (figsize=(20, 14))
                        
            xlabel ('Populations')
            ylabel ('Cache Hits/Misses')
            
            colors = gradient ("ff0000", "0000ff", len(self.Demos))
            for i in self.y_cache_hits:
                subplot (2, 2, i+1)
                xticks ( range(0, 128, self.x_step) )
                y_hits  = array (self.y_cache_hits[i])
                y_misses= array (self.y_cache_misses[i])
                plot (y_hits, color="#%s" % colors[i])
                plot (y_misses, "r:")
                grid (color='gray')
                #legend ()
            
            f.savefig ("%s/parallel_cache.png" % self.target)


def gradient(start, end, length):
    """ http://caioariede.com/2008/calculating-gradient-colors-with-python """
 
    # transform HEX to R G B
 
    __sr = int(start[0:2].upper(), 16) # 0
    __sg = int(start[2:4].upper(), 16) # 0
    __sb = int(start[4:6].upper(), 16) # 0
 
    __er = int(end[0:2].upper(), 16) # 255
    __eg = int(end[2:4].upper(), 16) # 255
    __eb = int(end[4:6].upper(), 16) # 255
 
    # calculate distance to make gradient
 
    stepr = (__er - __sr) / (length - 1) # 63
    stepg = (__eg - __sg) / (length - 1) # 63
    stepb = (__eb - __sb) / (length - 1) # 63
 
    # a color per step
 
    colors = [0] * length
 
    for i in range(0, length):
 
        if i == 0:
            # first color
            r = '%02X' % __sr
            g = '%02X' % __sg
            b = '%02X' % __sb
        elif i == length - 1:
            # last color
            r = '%02X' % __er
            g = '%02X' % __eg
            b = '%02X' % __eb
        else:
            # middle color
            r = '%02X' % (__sr + int(stepr) * i)
            g = '%02X' % (__sg + int(stepg) * i)
            b = '%02X' % (__sb + int(stepb) * i)
 
        colors[i] = r + g + b
 
    return colors

    