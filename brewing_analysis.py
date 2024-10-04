import numpy as np

class coffee_analysis():
    def __init__(self, x):
        if type(x) == float or type(x) == int:
            self.refr = np.array([float(x)])
        elif type(x) == list:
            self.refr = np.array(x)
        elif type(x) == np.ndarray:
            self.refr = x
        else:
            assert "Error, wrong data type"
    
    def tds_from_refr(self):
        self.tds = -662.0 * (self.refr - 1.3330) ** 2 + 549.5 * (self.refr - 1.3330) - 0.0396
        return self.tds

    def tds_integral(self):
        self.tds_from_refr()

        tdss = []
        
        for i in range(len(self.tds)):
            tdss.append(self.tds[:i].mean())
        return np.array(tdss)

    def mass_from_tds(self, bevarage):
        self.tds_from_refr()

        masses = np.zeros(len(self.tds))
        masses[0] = self.tds[0] * bevarage / 100

        for i in range(1, len(self.tds)):
            masses[i] = masses[i - 1] + self.tds[i] * bevarage / 100
    
        self.mass = np.array(masses)
        return self.mass
    
    def estimate(self, flows,  bevarage, coffee_mass):
        ey  = np.repeat((self.tds / (1 - self.tds / 100) *  bevarage/coffee_mass)[:len(flows)], repeats=flows).sum()
        tds = np.repeat(self.tds[:len(flows)], repeats=flows).mean()

        return ey, tds