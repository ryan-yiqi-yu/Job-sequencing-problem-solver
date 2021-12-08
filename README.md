# CS 170 Project Fall 2021

Requirements:

Python 3.6+

Files:
- `parse.py`: functions to read/write inputs and outputs
- `solver.py`: contains the solution to solve for all the outputs
- `Task.py`: contains a class that is useful for processing inputs

Precise instructions on how to run the solution algorithm:
1. The solution solver is contained in the solver.py file, therefore
in order to run the solution, you must be in the same directory.
2. In order for solver to run on the input files, there must be a folder
in its directory called 'inputs/'. Inside this folder, there must be
three sub-folders called 'small', 'medium', and 'large', where the respective
small medium and large '.in' files must be stored.
3. Create a folder 'outputs/' to hold outputs. Inside the outputs folder,
create a small/medium/large sub-folder. Output folders must be created in
order for the solution to run.
4. Once in the same directory as solver.py, run 'python3 solver.py'.
5. This command should run the solution on the given inputs and create outputs.
6. Wait for the program to finish running and you're finished.

# Job Sequencing Solution

Our approach to this problem consisted of several different algorithms. Listed below are the algorithms we incorporated into our final solution.

Our solution depended heavily on approaching the problem greedily. One of our algorithms involved was a greedy profit over duration algorithm. In this approach, we iteratively built our polishing schedule from start time 0 to the end, when no more tasks can fit into the 1440 time frame.  At every iteration step, we recalculate the profit/duration value--this is done because as we iteratively add tasks to our polishing schedule, the time progresses and some tasks can no longer be finished by its given deadline, which in turn decreases that task’s profit. Once all profit/duration values are recalculated, we greedily select the next task with the greatest profit/duration. We continue to iterate until there are no longer any tasks that can be completed before timestep 1440, indicating that the job schedule is complete and the algorithm terminates. This yields a greedy profit/duration schedule.

Next, we varied the greedy profit over duration algorithm above, yielding more greedy algorithms to further optimize our solution. In one of our variants, rather than greedily selecting profit/duration at every iteration, we greedily selected for raw profit: this algorithm is greedy profit. In yet another variant, we iteratively scheduled tasks backwards; that is, we started scheduling tasks from end to start (1440 to 0) and calculated task profits according to the time at each backwards step. In this reverse scheme, we yielded 2 more greedy algorithms by using 2 heuristics: greedily selecting the greatest profit/duration at each step, and greedily selecting for the greatest raw profit at each step. These 2 greedy algorithms are reverse greedy profit over duration and reverse greedy profit.

In total, the above algorithms had four variants: greedy profit over duration, greedy profit, reverse greedy profit over duration, and  reverse greedy profit.

This job scheduling problem has parallels to the knapsack problem. However, this problem involves an added element of profit decay, which the dynamic programming knapsack optimal solution does not account for. We relax our requirements and choose to ignore the decay in this specific algorithm. We perform dynamic programming knapsack on the input with respect to maximizing the (maximum profit)/(duration) of the total selected tasks. We blackbox knapsack by limiting our schedule to 1440 minutes and maximizing the profit/duration of tasks that fit within this time frame. Then, with the schedule returned by knapsack, which is in no particular order, we intentionally order it and sort by each task’s profit/duration, from greatest to least. 

Our final algorithm is a hybrid approach, combining and utilizing all the algorithms mentioned above. Our approach runs all the above algorithms on the given input and records each schedule outputted by the algorithms. We then refine and optimize the output schedules in order to reach a higher maximum profit. To optimize each schedule, we randomly varied the task orders. We adjusted the task order by randomly selecting 2 tasks in the schedule, swapping them, and finding the profit after the swap. If profit increased post-swap, we kept the post-swapped schedule. We randomly varied the schedule for a constant number of times and kept the maximum profit schedule of all the iterations--this is the optimized schedule. Then, we sort all the optimized schedules and select the schedule with the greatest output profit. This schedule is returned from our solution.

This is a good approach because using all the algorithms in a hybrid approach offers a decent amount of entropy in finding the global maximal profit. That is, if we were to optimize a single schedule, that schedule may reach a maximum which is not global, i.e. the maximum schedule given all possible schedule permutations. Instead, a maximum derived from a single schedule is only maximum to the given combination of tasks in the schedule; it is a local maxima. Therefore, using all our algorithms to produce unique schedules gives us a significant amount of variety to begin our search for maximum profits, increasing our chances of finding the global maxima, or at least a very close local maxima.
