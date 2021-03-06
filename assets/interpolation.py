import numpy as np
import pandas as pd

from numpy.linalg import norm as norm

def interpolate(df, H, W):
	RADIUS = int(W/2.5)
	cols = df.columns
	for index,column in enumerate(cols):
		if(index < 5): # Blue side
			cols_team = list(cols)[:5]
		else: # Red side
			cols_team = list(cols)[5:]

		cols_team.remove(column)
		col = df[column]
		col = np.array(col)
		colt = np.concatenate(col)
		
		# If no points found, usually caused by a bug in champion identification
		if(np.all(np.all(np.isnan(colt)))): 
			df[column] = [(np.nan,np.nan)]*len(col)
		else:
			col_temp = col
			i = 0

			# Search through points until an actual location is found
			while(np.all(np.isnan(col[i]))):
				i += 1

			# If there are missing values at the start
			if(np.all(np.isnan(col[0]))):
				try: # Need to fix
					temp = 20
					found = False
					
					# Check every champion on the same team to see if any were near the first known location
					for col_team in cols_team:
						for n in range(5): #4 seconds either side
							check = norm(df[col_team][i-n] - col[i])
							if(check < temp):
								temp = check
								found = True
								champ_found = col_team
							check = norm(df[col_team][i+n] - col[i])
							if(check < temp):
								temp = check
								found = True
								champ_found = col_team
					# If an ally was found near the first known location
					if(found):
						# Assume the two walked together
						col_temp = pd.concat([df[champ_found][:i],(col[i:])])
				except:
					pass

			j = len(col)-1

			# Same thing for missing values at the end
			while(np.all(np.isnan(col[j]))):
				j -= 1
			if(np.all(np.isnan(col[len(col)-1]))):
				try:
					temp = 20
					found = False
					for col_team in cols_team:
						for n in range(5):
							check = norm(df[col_team][j-n] - col[j])
							if(check < temp):
								temp = check
								found = True
								champ_found = col_team
							check = norm(df[col_team][j+n] - col[j])
							if(check < temp):
								temp = check
								found = True
								champ_found = col_team
					if(found):
						col_temp = pd.concat([(col_temp[:j+1]),(df[champ_found][j+1:])])
				except:
					pass

			count = 0
			k = i
			col_temp2 = col_temp

			# Deal with large chunks of missing values in the middle
			while(k < len(col_temp2)-1):
				k+=1
				if(np.all(np.isnan(col_temp[k]))):
					count += 1
				else:
					if(count > 5): # Missing for more than 5 seconds
						point = col_temp[k]
						if(index < 5): # Blue Side
							circle_x = 0
							circle_y = H
						else: # Red Side
							circle_x = W
							circle_y = 0
						# If first location after disappearing is in the base
						if(norm(np.array(point) - np.array([circle_x,circle_y])) < RADIUS):
							# Fill in with location just before disappearing (Assuming they died/recalled)
							col_temp2 = pd.concat([pd.Series(col_temp2[:k-count]),
											pd.Series([col_temp2[k-count-1]]*count),
											pd.Series(col_temp2[k:])], ignore_index = True)
						# Otherwise, check if there were any allies nearby before and after disappearing
						else:
							closest = 20
							found_closest = False

							# For every ally champion
							for col_team in cols_team:
								temp = 20
								found = False
								for i in range(5):
									try:
										check = norm(np.array(point) - np.array(df[col_team][k+i]))
										if(check < temp):
											temp = check
											found = True

										check = norm(np.array(point) - np.array(df[col_team][k-i]))
										if(check < temp):
											temp = check
											found = True
									except:
										pass

								# If ally found nearby just before disappearing
								if(found):
									temp2 = 20
									for i in range(5):
										try:											
											check2 = norm(np.array(col_temp[k-count-1]) - np.array(df[col_team][k-count-1+i]))
											if(check2 < temp2):
												temp2 = check2
												found_closest = True

											check2 = norm(np.array(col_temp[k-count-1]) - np.array(df[col_team][k-count-1-i]))
											if(check2 < temp2):
												temp2 = check2
												found_closest = True
										except:
											pass

								# If ally found nearby before and after disappearing
								if(found_closest):
									# Choose ally who was closest on average
									average = (temp + temp2) / 2
									if(average < closest):
										closest = average
										champ_found = col_team

							# Assume the two walked together
							if(found_closest):
								col_temp2 = pd.concat([pd.Series(col_temp2[:k-count]),
												df[champ_found][k-count:k],
												pd.Series(col_temp2[k:])],ignore_index = True)
					count = 0
			df[column] = col_temp2
	for col in df.columns: ###########
		df[col] = list(zip(*map(
			lambda l: l.interpolate().round(),
			list(
				map(pd.Series, 
				zip(*df[col]))))))
	return(df)