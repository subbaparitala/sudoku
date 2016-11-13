from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError, Http404
from django.shortcuts import get_object_or_404, render, render_to_response
from django.core.urlresolvers import reverse
from django.views import generic
from solution import Solution
from django.core.context_processors import csrf
from random import randint


def input_sudoku(request):
	entrada = []
	mode = request.GET.get('mode')
	mode = int(mode)*9 or 9
	
	for i in range(0, 81):
		entrada.append('.')
	sorter = []
	for i in range(0,mode):
		sorter.append(randint(0,80))

	entrada[randint(1,9)] = randint(1,9)
	entrada[randint(1,9)] = randint(1,9)
	print entrada
	solution = Solution(entrada).return_grid()

	
	c = { 'solution' : solution, 'sorter': sorter}
	c.update(csrf(request))
	return render_to_response('solve/input.html', c)

def no_solution(request):
	return render(request, 'solve/unsolvable.html')

def solve_sudoku(request):
	sudoku_input = []
	for i in range(0, 81):
		input_character = request.POST[str(i)]
		if len(input_character) == 0:
			sudoku_input.append('.')
		else:
			sudoku_input.append(input_character)
	print sudoku_input
	sudoku_solution = Solution(sudoku_input).return_grid()

	# Save session to display the contents of the solution of the sudoku
	# in the display_sudoku view
	# Always redirect after POST.
	request.session['sudoku_solution'] = repr(sudoku_solution)

	if not sudoku_solution:
		return HttpResponseRedirect(reverse('solve:no_solution'))
	else:
		return HttpResponseRedirect(reverse('solve:display'))

def display_sudoku(request):
	sudoku_solution = request.session.get('sudoku_solution', None)

	if sudoku_solution is not None:
		sudoku_solution = eval(sudoku_solution)
	else:
		return HttpResponseRedirect(reverse('solve:no_solution'))

	return render(request, 'solve/display.html', {"grid":sudoku_solution})
