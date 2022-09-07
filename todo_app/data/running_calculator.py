from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import fsolve
import mpld3
from todo_app.data.strava_client import StravaClient

MIN_DISTANCE, MAX_DISTANCE = 1500, 30000
class RunningCalculator:
  def __init__(self):
    self.user_vdot = 50

  def set_vdot(self, distance, pace):
    self.user_vdot = self.calc_vdot(distance, pace)

  def get_pace(self, distance,vdot):
    # distance in m
    [a,b,c,d,e,f,g,h,i,j] = [ 2.12585218e-12, -1.06457439e-03,  5.77331309e-10,  1.70220844e-07,
      -2.07683704e-07,  2.45502883e-01, -5.75823885e-05,  7.58905732e-03,
      -2.06038745e+01,  7.62475662e+02]
    return a * distance**3 + b * vdot**3 + c*distance**2*vdot + d*distance*vdot**2 + e*distance**2 + f*vdot**2 + g*distance*vdot + h*distance + i*vdot + j

  def calc_vdot(self, input_distance, pace):
      if input_distance < MIN_DISTANCE or input_distance > MAX_DISTANCE:
          raise ValueError("Enter distance between 1500m and 30k")

      def pace_func(vdot):
        return pace - self.get_pace(input_distance, vdot)

      vdot = fsolve(pace_func, 50)
      return vdot[0]

  def calc_relative_effort(self, vdot, distance, time):
      pace = 1000 * time / distance
      max_pace = self.get_pace(distance, vdot)
      return max_pace / pace

  def get_interval_relative_efforts(self, id):
      strava_client = StravaClient()
      laps = strava_client.get_activity_laps(id)
      relative_efforts = np.array([self.calc_relative_effort(self.user_vdot, lap["distance"], lap["elapsed_time"]) for lap in laps])
      return relative_efforts
      key_laps = [effort > 0.8 for effort in relative_efforts]
      condensed_laps = []
      current_sum_dist = 0
      current_sum_time = 0
      for (key, lap) in zip(key_laps, laps):
        if key:
          current_sum_dist += lap["distance"]
          current_sum_time += lap["elapsed_time"]
        else:
          if current_sum_time > 0 and current_sum_dist > 0:
            condensed_laps.append({
              "distance": current_sum_dist,
              "elapsed_time": current_sum_time
            })
            current_sum_time, current_sum_dist = 0, 0
          else:
            continue
      return np.array([self.calc_relative_effort(self.user_vdot, lap["distance"], lap["elapsed_time"]) for lap in condensed_laps])

  def plot_session(self, id):
      session = self.get_interval_relative_efforts(id)

      plt.bar(range(len(session)), session)
      plt.xlabel('Lap number')
      plt.ylabel('Relative performance')
      fig = plt.gcf()
      plt_html = mpld3.fig_to_html(fig)
      plt.close()
      return plt_html

  def plot_sessions(self, ids):
      print(ids)
      ids.reverse()
      sessions = []
      averages = []
      for id in ids:
          session = self.get_interval_relative_efforts(id)
          if len(session) == 0:
              continue
          session_average = sum(session)/len(session);
          averages.append(session_average)
          sessions.append(session)

      plt.plot(averages)
      plt.xlabel("Session number")
      plt.ylabel("Relative performance avg")
      fig = plt.gcf()
      plt_html = mpld3.fig_to_html(fig)
      plt.close()
      return plt_html