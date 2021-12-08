from parse import read_input_file, write_output_file, read_output_file
import os
import random
from math import comb

## TODO: Implement job sequencing problem (without loss function) optimum solution:
## https://stackoverflow.com/questions/61352269/job-sequencing-problem-with-three-parameters

## Other ideas?:
## Approximate loss function to a linear loss, along the lines of
## section 2 in this paper and schedule tasks:
## https://www.jstor.org/stable/2627472?refreqid=excelsior%3A6c40ea3d138a20095d15792036568ea7
##
## https://stackoverflow.com/questions/33184070/job-scheduling-to-minimise-loss/54445784


"""
Task object example:
t1 = Task.Task(1, 2, 3, 4.0)
Args:
    - task_id (int): task id of the Task
    - deadline (int): deadline of the Task
    - duration (int): duration of the Task
    - perfect_benefit (float): the benefit recieved from completing the Task
      anytime before (or on) the deadline
GET Sample usage:
    task0.get_task_id()
    task0.get_deadline()
    task0.get_duration()
    task0.get_max_benefit()
    task0.get_late_benefit(0) -> 3.0
    task0.get_late_benefit(5) -> 2.7555368532043722
    task0.get_late_benefit(30) -> 1.8014867364367977
"""


def dp_knapsack(tasks):
    ##recurrence relation: R(n, W) = max(val[n] + R(n -1, W-wt[n]), R(n-1, W))
    ##grid[TIME][TASK]
    grid = [[0 for _ in range(len(tasks)+1)] for _ in range(1440+1)]
    path_grid = [[[] for _ in range(len(tasks)+1)] for _ in range(1440+1)]
    for task_i in range(1, len(tasks)+1):
        duration = tasks[task_i-1].get_duration()
        profit = tasks[task_i-1].get_max_benefit() #/ duration
        for time in range(1, 1441):
            if duration > time:
                continue
            include_profit = grid[time-duration][task_i - 1] + profit
            no_include_profit = grid[time][task_i - 1]
            if include_profit > no_include_profit:
                grid[time][task_i] = include_profit
                path_grid[time][task_i] = path_grid[time-duration][task_i - 1][:]
                path_grid[time][task_i].append(tasks[task_i-1])
            else:
                grid[time][task_i] = no_include_profit
                path_grid[time][task_i] = path_grid[time][task_i - 1][:]

    optimum_tasks = path_grid[1440][len(tasks)]
    optimum_tasks.sort(key=lambda x: x.get_max_benefit()/x.get_duration(), reverse=True)
    schedule = [task.get_task_id() for task in optimum_tasks]
    return schedule


def maxima_finder(tasks):
    schedule = []
    schedule_max = []
    time = 1440
    improve = True
    max_profit = 0
    attempted = []
    while improve:
        improve = False
        for _ in range(100000):
            tasks_copy = tasks[:]
            schedule = []
            while tasks_copy:
                i = random.randrange(len(tasks_copy))
                if time - tasks_copy[i].get_duration() >= 0:
                    schedule.append(tasks_copy[i].get_task_id())
                    time -= tasks_copy[i].get_duration()
                tasks_copy.pop(i)

            schedule_hash = hash(tuple(schedule))
            if schedule_hash in attempted:
                continue
            attempted.append(schedule_hash)
            profit = calculate_profit(schedule, tasks)
            if profit > max_profit:
                max_profit = profit
                schedule_max = schedule[:]
                improve = True
    return schedule_max



def maxima(schedule, tasks):
    improve = True
    schedule_max = schedule[:]
    schedule_copy = schedule[:]
    max_profit = calculate_profit(schedule, tasks)
    schedule_len = len(schedule_copy)
    iters = comb(schedule_len, 2)
    swaps = []
    ij = []
    for i in range(schedule_len):
        for j in range(schedule_len):
            if i == j and (i,j) in swaps or (j,i) in swaps:
                continue
            swaps.append((i,j))
    while improve:
        improve = False
        for _ in range(50*iters):
            i, j = random.choice(swaps)
            if (i,j) in ij or (j,i) in ij:
                continue
            ij.append((i,j))
            schedule_copy = schedule_max[:]
            schedule_copy[i], schedule_copy[j] = schedule_copy[j], schedule_copy[i]
            profit = calculate_profit(schedule_copy, tasks)
            if profit > max_profit:
                ij = []
                max_profit = profit
                schedule_max = schedule_copy[:]
                improve = True
                break
    return schedule_max




def greedy(tasks):
    schedule = []
    for task in tasks:
        tasks.remove(task)


def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing
    """
    #return greedy_recalculate_per_iteration(tasks)
    #return greedy_recalculation(tasks)
    #grid = [[None for _ in range(1440)] for _ in range(len(tasks))]
    #sched_grid = [[None for _ in range(1440)] for _ in range(len(tasks))]
    #profit, sched = dp_test(0, 0, tasks, grid, sched_grid, [])
    #print(profit)
    schedule1 = greedy_recalculate_per_iteration_backwards(tasks[:])
    schedule2 = greedy_recalculate_per_iteration_backwards_profit(tasks[:])
    schedule3 = greedy_recalculate_per_iteration(tasks[:])
    schedule4 = greedy_recalculate_per_iteration_profit(tasks[:])
    schedule5 = greedy(tasks[:])
    schedule7 = greedy_past_deadline(tasks[:])
    schedule_dict = {calculate_profit(schedule1, tasks):schedule1, calculate_profit(schedule2, tasks):schedule2,
    calculate_profit(schedule3, tasks):schedule3, calculate_profit(schedule4, tasks):schedule4, calculate_profit(schedule5, tasks):schedule5,
    calculate_profit(schedule7, tasks):schedule7}
    max_profit = max(schedule_dict, key=schedule_dict.get)
    max_schedule = maxima(schedule_dict[max_profit][:], tasks[:])
    if max_schedule == schedule1:
        print('p/d backwards')
    elif max_schedule == schedule2:
        print('p backwards')
    elif max_schedule == schedule3:
        print('p/d forwards')
    elif max_schedule == schedule4:
        print('p forward')
    elif max_schedule == schedule5:
        print('greedy')
    elif max_schedule == schedule7:
        print('greedy past')
    else:
        print('Maxima')



    return max_schedule
    """
    task_order = []
    for task in tasks:
        next_task
    """

def calculate_profit(schedule, tasks):
    tasks_dict = {task.get_task_id():task for task in tasks}
    time = 0
    profit = 0
    for task_id in schedule:
        task = tasks_dict[task_id]
        profit += task.get_late_benefit(task.get_duration() + time - task.get_deadline())
        time += task.get_duration()
    assert time <= 1440, 'too many tasks scheduled'
    return profit


def test(tasks):
    for task in tasks:
        print(task.get_late_benefit(1) == task.get_max_benefit())
    return [1]

def recalculate_benefit(tasks, time):
    return [(x.get_late_benefit(time + x.get_duration() - x.get_deadline()), x.get_duration(), abs(x.get_deadline()-time), x.get_task_id()) for _, x in tasks.items()]


def greedy_recalculate_per_iteration_backwards(tasks):
    deadline = 0
    time = 1440
    schedule = []
    tasks_dict = {task.get_task_id():task for task in tasks}
    while tasks_dict and time > 0:
        task_benefits = recalculate_benefit(tasks_dict, time)
        max_benefit = max(task_benefits, key=lambda x: x[0]/x[1])
        if time + max_benefit[1] > 1440:
            time -= 1
            continue
        elif time - max_benefit[1] < 0:
            break
        schedule.append(max_benefit[3])
        time -= max_benefit[1]
        tasks_dict.pop(max_benefit[3])
    return schedule[::-1]

def greedy_recalculate_per_iteration_backwards_profit(tasks):
    deadline = 0
    time = 1440
    schedule = []
    tasks_dict = {task.get_task_id():task for task in tasks}
    while tasks_dict and time > 0:
        task_benefits = recalculate_benefit(tasks_dict, time)
        max_benefit = max(task_benefits, key=lambda x: x[0])
        if time + max_benefit[1] > 1440:
            time -= 1
            continue
        elif time - max_benefit[1] < 0:
            break
        schedule.append(max_benefit[3])
        time -= max_benefit[1]
        tasks_dict.pop(max_benefit[3])
    return schedule[::-1]

def greedy_recalculate_per_iteration(tasks):
    deadline = 1440
    time = 0
    schedule = []
    tasks_dict = {task.get_task_id():task for task in tasks}
    while tasks_dict:
        task_benefits = recalculate_benefit(tasks_dict, time)
        max_benefit = max(task_benefits, key=lambda x: x[0]/x[1])
        if time + max_benefit[1] <= deadline:
            schedule.append(max_benefit[3])
            time += max_benefit[1]
        tasks_dict.pop(max_benefit[3])
    return schedule


def greedy_recalculate_per_iteration_profit(tasks):
    deadline = 1440
    time = 0
    schedule = []
    tasks_dict = {task.get_task_id():task for task in tasks}
    while tasks_dict:
        task_benefits = recalculate_benefit(tasks_dict, time)
        max_benefit = max(task_benefits, key=lambda x: x[0])
        if time + max_benefit[1] <= deadline:
            schedule.append(max_benefit[3])
            time += max_benefit[1]
        tasks_dict.pop(max_benefit[3])
    return schedule

def greedy_past_deadline(tasks):
    current_time = 0
    schedule = []
    while True:
        possible_next_tasks = tasks
        # deadline: 1000, finished: 100 -> 0
        # deadline: 200, finished: 500 -> 300
        # max(finished - deadline, 0)
        possible_next_tasks.sort(key=lambda x: x.get_late_benefit(max(0, current_time + x.get_duration() - x.get_deadline())) / x.get_duration(), reverse=True)

        next_task_picked = False
        for possible_next_task in possible_next_tasks:
            if possible_next_task.get_duration() + current_time <= 1440:
                schedule.append(possible_next_task.get_task_id())
                current_time += possible_next_task.get_duration()
                next_task_picked = True
                tasks.remove(possible_next_task)
                break

        if current_time >= 1440:
            break

        if next_task_picked == False:
            current_time += 1
            continue

    return schedule

def greedy(tasks):
    current_time = 0
    schedule = []
    while True:
        possible_next_tasks = [task for task in tasks if task.get_deadline() > current_time and task.get_deadline() <= current_time + 60]
        possible_next_tasks.sort(key=lambda x: x.get_max_benefit() / x.get_duration(), reverse=True)

        next_task_picked = False
        for possible_next_task in possible_next_tasks:
            if possible_next_task.get_duration() + current_time <= possible_next_task.get_deadline() and possible_next_task.get_duration() + current_time <= 1440:
                schedule.append(possible_next_task.get_task_id())
                current_time += possible_next_task.get_duration()
                next_task_picked = True
                tasks.remove(possible_next_task)
                break

        if current_time >= 1440:
            break

        if next_task_picked == False:
            current_time += 1
            continue

    return schedule


def greedy_profitOverDuration(tasks):
    tasks.sort(key=lambda x: x.get_max_benefit()/x.get_duration(), reverse=True)
    time = 1440
    schedule = []
    for task in tasks:
        time -= task.get_duration()
        if time >= 0:
            schedule.append(task.get_task_id())
        else:
            break
    return schedule


def recalibrate_output():
    for size in os.listdir('outputs/'):
        if size not in ['small', 'medium', 'large']:
            continue
        for output_file in os.listdir('outputs/{}/'.format(size)):
            if size not in output_file:
                continue
            output_path = 'outputs/{}/{}'.format(size, output_file)
            input_path = 'inputs/{}/{}.in'.format(size, output_file[:-4])
            print('Optimizing ...', input_path, output_path)
            schedule = read_output_file(output_path)
            tasks = read_input_file(input_path)
            test_schedule = greedy_recalculate_per_iteration_backwards(tasks[:])
            max_schedule = maxima(test_schedule[:], tasks[:])
            if calculate_profit(max_schedule, tasks) > calculate_profit(schedule,tasks):
                print(calculate_profit(max_schedule, tasks) - calculate_profit(schedule,tasks))
                write_output_file(output_path, max_schedule)


def absolute_maxima_approx():
    for size in os.listdir('inputs/'):
        if size not in ['small', 'medium', 'large']:
            continue
        for input_file in os.listdir('inputs/{}/'.format(size)):
            if size not in input_file:
                continue
            output_path = 'outputs/{}/{}.out'.format(size, input_file[:-3])
            input_path = 'inputs/{}/{}'.format(size, input_file)
            print(input_path, output_path)
            tasks = read_input_file(input_path)
            schedule1 = maxima(greedy_recalculate_per_iteration_backwards(tasks[:]),tasks[:])
            schedule2 = maxima(greedy_recalculate_per_iteration_backwards_profit(tasks[:]),tasks[:])
            schedule3 = maxima(greedy_recalculate_per_iteration(tasks[:]),tasks[:])
            schedule4 = maxima(greedy_recalculate_per_iteration_profit(tasks[:]),tasks[:])
            schedule5 = maxima(dp_knapsack(tasks[:]),tasks[:])
            schedule6 = maxima(maxima_finder(tasks[:]),tasks[:])
            schedule_dict = {calculate_profit(schedule1, tasks[:]):schedule1, calculate_profit(schedule2, tasks[:]):schedule2,
            calculate_profit(schedule3, tasks[:]):schedule3, calculate_profit(schedule4, tasks[:]):schedule4,
            calculate_profit(schedule5, tasks[:]):schedule5, calculate_profit(schedule6, tasks[:]):schedule6}
            max_profit = max(schedule_dict, key=schedule_dict.get)
            max_schedule = schedule_dict[max_profit]
            write_output_file(output_path, max_schedule)

# Here's an example of how to run your solver.
#if __name__ == '__main__':
def main():
     for size in os.listdir('inputs/'):
         if size not in ['small', 'medium', 'large']:
             continue
         for input_file in os.listdir('inputs/{}/'.format(size)):
             if size not in input_file:
                 continue
             input_path = 'inputs/{}/{}'.format(size, input_file)
             output_path = 'outputs/{}/{}.out'.format(size, input_file[:-3])
             print(input_path, output_path)
             tasks = read_input_file(input_path)
             output = solve(tasks)
             write_output_file(output_path, output)

if __name__ == '__main__':
    #absolute_maxima_approx()
    recalibrate_output()
