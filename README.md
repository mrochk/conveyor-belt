# Conveyor Belt Optimization
What is the optimal way to arrange a cart of items on a supermarket conveyor belt? 

This problem is actually the problem of placing a set of shapes $S$ into a rectangle $r$ for which $area(r) \geq \sum_{s \in S}{area(s)}$... [Tetris](https://en.wikipedia.org/wiki/Tetris) actually.

Here is how I proceeded:

1. Assuming a supermarket conveyor belt is $100$ cm wide, divide it into $n$ squares (here I chose to divide it into 4 squares per row $\implies$ each square is of size $25 \times 25$). 
2. To simplify as much as possible, assume each item is given to us as a rectangle seen from the sky, (as the minimum-sized rectangle that can hold the item), transform it into another rectangle made of squares of width $\frac{100}{n}$.
3. Now that we have a set of shape made of squares of size $\frac{100}{n} \times \frac{100}{n}$, we could just recursively try every possible ways of putting them in $r$ and return the combination that takes the minimum length, but that would be very inneficient. Instead, observe that if we have a rectangle in the form $(4, x)$ it is always going to be the optimal shape to put first, so, while we have either rectangles having this form, or that we can assemble multiple smaller rectangles to create a bigger rectangle having this form, we can place them. 
4. For the rest of the shapes (often very few compared to the beginning) we can just try every possible ways of placing them and keep the one which has the smallest length.

TO-DO:\
My code works for most cases, but to get the best result, we must prioritize certain shapes in the form $(4, x)$ over others, the ones using the bigger rectangles, e.g: $((2, 3), (2, 3)) > ((1, 1), (1, 1), (1, 1), (1, 1))$. 