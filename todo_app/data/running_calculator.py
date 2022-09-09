from cProfile import label
from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import fsolve
from mpld3 import fig_to_html, plugins
from todo_app.data.strava_client import StravaClient
import datetime

MIN_DISTANCE, MAX_DISTANCE = 1500, 30000
class RunningCalculator:
  def __init__(self):
    self.strava_client = StravaClient()
    self.user_vdot = 50
    self.user_threshold = self.calc_threshold_speed(self.user_vdot)
    self.user_work_capacity = self.calc_work_capacity(self.user_vdot, 5000, 239)

  def set_vdot(self, distance, pace):
    self.user_vdot = self.calc_vdot(distance, pace)
    self.user_threshold = self.calc_threshold_speed(self.user_vdot)
    self.user_work_capacity = self.calc_work_capacity(self.user_vdot, distance, pace)

  def get_pace(self, distance,vdot):
    # distance in m
    [a,b,c,d,e,f,g,h,i,j] = [ 2.12585218e-12, -1.06457439e-03,  5.77331309e-10,  1.70220844e-07,
      -2.07683704e-07,  2.45502883e-01, -5.75823885e-05,  7.58905732e-03,
      -2.06038745e+01,  7.62475662e+02]
    return a * distance**3 + b * vdot**3 + c*distance**2*vdot + d*distance*vdot**2 + e*distance**2 + f*vdot**2 + g*distance*vdot + h*distance + i*vdot + j

  def calc_threshold_speed(self, vdot):
    return 1000 / self.get_pace(16000, vdot)

  def calc_speed_from_pace(self, pace):
    return 1000 / pace

  def calc_work_capacity(self, vdot, distance, pace):
    speed = self.calc_speed_from_pace(pace)
    time = distance / speed
    return (speed - self.calc_threshold_speed(vdot)) * time

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

  def analyse_activity(self, id):
    laps = self.strava_client.get_activity_laps(id)
    w_primes = self.get_work_values(laps)
    return laps, w_primes

  def get_work_values(self, laps):
    w_primes = [self.user_work_capacity]
    for lap in laps:
      work_done = self.calc_work_capacity_diff(lap["moving_time"], lap["average_speed"], w_primes[-1])
      w_prime = min(w_primes[-1] + work_done, self.user_work_capacity)
      w_primes.append(w_prime)
    return w_primes

  def calc_work_capacity_diff(self, time, speed, w_prime):
    w_t = self.user_work_capacity
    threshold = self.user_threshold
    # negative for above threshold work, positive for below
    if (speed > threshold):
      # above threshold
      return time * (threshold - speed)
    else:
      # below threshold:
      dw_initial = time * (threshold - speed) * ((w_t - w_prime)/w_t)
      dw_final = time * (threshold - speed) * ((w_t - (w_prime + dw_initial))/w_t)
      return (dw_initial + dw_final) / 2


  def plot_session(self, id):
      laps, w_primes = self.analyse_activity(id)

      fig, ax = plt.subplots()

      # ax2 = ax.twinx()
      ax.plot(range(len(w_primes)), w_primes)
      paces = ax.bar([lap['lap_index'] - 0.5 for lap in laps], [lap['average_speed'] * 50 for lap in laps], color='r', alpha=0.5, width=0.95)
      ax.set(xlabel='Lap number', ylabel="W'")

      xlabels = []
      for i, lap in enumerate(laps):
        lap_pace = round(1000 * lap["moving_time"] / lap["distance"], 0)
        region_label = f"{round(lap['distance'] / 1000, 2)}km @ {datetime.timedelta(seconds=lap_pace)}"
        xlabels.append(region_label)
        ax.axvspan(i, i+1, label=region_label, alpha=0)

      ax.set_xticks(range(len(xlabels)))
      ax.bar_label(paces, labels=xlabels, label_type='center', padding=0, rotation=90, position=(-90, -30))

      # ax.legend(loc='right')
      
      # fig = plt.gcf()
      fig.set_size_inches(10, 7)

      plt_html = fig_to_html(fig)
      plt.close()
      return plt_html

  # def plot_session(self, id):
  #     session = self.get_interval_relative_efforts(id)

  #     plt.plot(range(len(session)), session)
  #     plt.xlabel('Lap number')
  #     plt.ylabel('Relative performance')
  #     fig = plt.gcf()
  #     plt_html = mpld3.fig_to_html(fig)
  #     plt.close()
  #     return plt_html

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
      plt_html = fig_to_html(fig)
      plt.close()
      return plt_html