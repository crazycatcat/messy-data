from numpy import array
from numpy import mean, median, ptp, var, std,cov, corrcoef

def desStat(data):
	mean=mean(data)
	medi=median(data)
	rangeptp=ptp(data)
	var=var(data)
	std=std(data)
	#cov=cov(data)
	#corrf=corrcoef(data)
	return self.mean,self.medi,self.rangeptpself.var,self.std
	