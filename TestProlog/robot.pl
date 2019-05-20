/* recherche dans un graphe d'etats */

/*recherche(EtatCourant,EtatFinal,ListeTaboue,ListeOp) tous donnes sauf ListeOp */
recherche(Ec,Ec,_,[]):-!.
recherche(Ec,Ef,Ltaboue,[Op|Lop]) :- 
	operateur(Ec,Op,Es),
	not(member(Es,Ltaboue)),
	%write(Ec), write(' '), write(Op), write(' '),write(Es),nl,
	recherche(Es,Ef,[Es|Ltaboue],Lop).

resoudre(Sol) :- etatInitial(Ei),etatFinal(Ef),
	recherche(Ei,Ef,[Ei],Sol).

/* probleme du labyrinthe */

% Etat décrit par: position des 3 robot ( 3 arg ) et leur orientation
etatInitial([0,0,up,0,7,up,7,0,up]).
etatFinal([1,3,up,4,5,up,6,7,up]).

linked([0,0],[1,0]).
linked([0,0],[0,1]).
linked([0,1],[1,1]).
linked([0,1],[0,2]).
linked([0,1],[0,0]).
linked([0,2],[1,2]).
linked([0,2],[0,3]).
linked([0,2],[0,1]).
linked([0,3],[1,3]).
linked([0,3],[0,4]).
linked([0,3],[0,2]).
linked([0,4],[1,4]).
linked([0,4],[0,5]).
linked([0,4],[0,3]).
linked([0,5],[1,5]).
linked([0,5],[0,6]).
linked([0,5],[0,4]).
linked([0,6],[1,6]).
linked([0,6],[0,7]).
linked([0,6],[0,5]).
linked([0,7],[1,7]).
linked([0,7],[0,6]).
linked([1,0],[2,0]).
linked([1,0],[0,0]).
linked([1,0],[1,1]).
linked([1,1],[2,1]).
linked([1,1],[0,1]).
linked([1,1],[1,2]).
linked([1,1],[1,0]).
linked([1,2],[2,2]).
linked([1,2],[0,2]).
linked([1,2],[1,3]).
linked([1,2],[1,1]).
linked([1,3],[0,3]).
linked([1,3],[1,4]).
linked([1,3],[1,2]).
linked([1,4],[2,4]).
linked([1,4],[0,4]).
linked([1,4],[1,5]).
linked([1,4],[1,3]).
linked([1,5],[2,5]).
linked([1,5],[0,5]).
linked([1,5],[1,6]).
linked([1,5],[1,4]).
linked([1,6],[2,6]).
linked([1,6],[0,6]).
linked([1,6],[1,7]).
linked([1,6],[1,5]).
linked([1,7],[2,7]).
linked([1,7],[0,7]).
linked([1,7],[1,6]).
linked([2,0],[3,0]).
linked([2,0],[1,0]).
linked([2,0],[2,1]).
linked([2,1],[3,1]).
linked([2,1],[1,1]).
linked([2,1],[2,2]).
linked([2,1],[2,0]).
linked([2,2],[3,2]).
linked([2,2],[1,2]).
linked([2,2],[2,3]).
linked([2,2],[2,1]).
linked([2,3],[3,3]).
linked([2,3],[2,4]).
linked([2,3],[2,2]).
linked([2,4],[3,4]).
linked([2,4],[1,4]).
linked([2,4],[2,5]).
linked([2,4],[2,3]).
linked([2,5],[3,5]).
linked([2,5],[1,5]).
linked([2,5],[2,6]).
linked([2,5],[2,4]).
linked([2,6],[3,6]).
linked([2,6],[1,6]).
linked([2,6],[2,7]).
linked([2,6],[2,5]).
linked([2,7],[3,7]).
linked([2,7],[1,7]).
linked([2,7],[2,6]).
linked([3,0],[4,0]).
linked([3,0],[2,0]).
linked([3,0],[3,1]).
linked([3,1],[4,1]).
linked([3,1],[2,1]).
linked([3,1],[3,2]).
linked([3,1],[3,0]).
linked([3,2],[4,2]).
linked([3,2],[2,2]).
linked([3,2],[3,3]).
linked([3,2],[3,1]).
linked([3,3],[4,3]).
linked([3,3],[2,3]).
linked([3,3],[3,4]).
linked([3,3],[3,2]).
linked([3,4],[4,4]).
linked([3,4],[2,4]).
linked([3,4],[3,5]).
linked([3,4],[3,3]).
linked([3,5],[4,5]).
linked([3,5],[2,5]).
linked([3,5],[3,6]).
linked([3,5],[3,4]).
linked([3,6],[4,6]).
linked([3,6],[2,6]).
linked([3,6],[3,7]).
linked([3,6],[3,5]).
linked([3,7],[4,7]).
linked([3,7],[2,7]).
linked([3,7],[3,6]).
linked([4,0],[5,0]).
linked([4,0],[3,0]).
linked([4,0],[4,1]).
linked([4,1],[5,1]).
linked([4,1],[3,1]).
linked([4,1],[4,2]).
linked([4,1],[4,0]).
linked([4,2],[3,2]).
linked([4,2],[4,3]).
linked([4,2],[4,1]).
linked([4,3],[5,3]).
linked([4,3],[3,3]).
linked([4,3],[4,4]).
linked([4,3],[4,2]).
linked([4,4],[5,4]).
linked([4,4],[3,4]).
linked([4,4],[4,5]).
linked([4,4],[4,3]).
linked([4,5],[5,5]).
linked([4,5],[3,5]).
linked([4,5],[4,6]).
linked([4,5],[4,4]).
linked([4,6],[5,6]).
linked([4,6],[3,6]).
linked([4,6],[4,7]).
linked([4,6],[4,5]).
linked([4,7],[5,7]).
linked([4,7],[3,7]).
linked([4,7],[4,6]).
linked([5,0],[6,0]).
linked([5,0],[4,0]).
linked([5,0],[5,1]).
linked([5,1],[6,1]).
linked([5,1],[4,1]).
linked([5,1],[5,0]).
linked([5,2],[6,2]).
linked([5,2],[5,3]).
linked([5,3],[6,3]).
linked([5,3],[4,3]).
linked([5,3],[5,4]).
linked([5,3],[5,2]).
linked([5,4],[6,4]).
linked([5,4],[4,4]).
linked([5,4],[5,5]).
linked([5,4],[5,3]).
linked([5,5],[4,5]).
linked([5,5],[5,4]).
linked([5,6],[6,6]).
linked([5,6],[4,6]).
linked([5,6],[5,7]).
linked([5,7],[6,7]).
linked([5,7],[4,7]).
linked([5,7],[5,6]).
linked([6,0],[7,0]).
linked([6,0],[5,0]).
linked([6,0],[6,1]).
linked([6,1],[7,1]).
linked([6,1],[5,1]).
linked([6,1],[6,2]).
linked([6,1],[6,0]).
linked([6,2],[7,2]).
linked([6,2],[5,2]).
linked([6,2],[6,3]).
linked([6,2],[6,1]).
linked([6,3],[7,3]).
linked([6,3],[5,3]).
linked([6,3],[6,4]).
linked([6,3],[6,2]).
linked([6,4],[7,4]).
linked([6,4],[5,4]).
linked([6,4],[6,5]).
linked([6,4],[6,3]).
linked([6,5],[7,5]).
linked([6,5],[6,6]).
linked([6,5],[6,4]).
linked([6,6],[7,6]).
linked([6,6],[5,6]).
linked([6,6],[6,7]).
linked([6,6],[6,5]).
linked([6,7],[7,7]).
linked([6,7],[5,7]).
linked([6,7],[6,6]).
linked([7,0],[6,0]).
linked([7,0],[7,1]).
linked([7,1],[6,1]).
linked([7,1],[7,0]).
linked([7,2],[6,2]).
linked([7,2],[7,3]).
linked([7,3],[6,3]).
linked([7,3],[7,4]).
linked([7,3],[7,2]).
linked([7,4],[6,4]).
linked([7,4],[7,5]).
linked([7,4],[7,3]).
linked([7,5],[6,5]).
linked([7,5],[7,6]).
linked([7,5],[7,4]).
linked([7,6],[6,6]).
linked([7,6],[7,7]).
linked([7,6],[7,5]).
linked([7,7],[6,7]).
linked([7,7],[7,6]).

% Operateur XYZ -> X action du 1e robot, Y action du second, Z action du 3e
% X, Y, Z [X1, Y1, D1, X2, Y2, D2, X3, Y3, D3]uvent prendre les valeurs A, L, R, W pour advance, go left, go right et wait
operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], aaa, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    avancer(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    avancer(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    avancer(D3, [X3, Y3], NewD3, [NewX3, NewY3]).
    
operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], aal, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    avancer(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    avancer(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    left(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], aar, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    avancer(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    avancer(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    right(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], aaw, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    avancer(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    avancer(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    wait(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], ala, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    avancer(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    left(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    avancer(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], all, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    avancer(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    left(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    left(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], alr, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    avancer(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    left(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    right(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], alw, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    avancer(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    left(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    wait(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], ara, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    avancer(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    right(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    avancer(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], arl, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    avancer(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    right(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    left(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], arr, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    avancer(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    right(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    right(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], arw, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    avancer(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    right(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    wait(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], awa, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    avancer(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    wait(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    avancer(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], awl, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    avancer(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    wait(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    left(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], arw, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    avancer(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    right(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    wait(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], aww, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    avancer(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    wait(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    wait(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], laa, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    left(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    avancer(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    avancer(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], lal, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    left(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    avancer(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    left(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], lar, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    left(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    avancer(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    right(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], law, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    left(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    avancer(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    wait(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], lla, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    left(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    left(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    avancer(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], lll, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    left(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    left(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    left(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], llr, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    left(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    left(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    right(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], llw, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    left(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    left(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    wait(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], lra, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    left(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    right(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    avancer(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], lrl, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    left(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    right(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    left(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], lrr, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    left(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    right(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    right(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], lrw, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    left(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    right(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    wait(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], lwa, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    left(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    wait(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    avancer(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], lwl, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    left(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    wait(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    left(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], lwr, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    left(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    wait(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    right(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], lww, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    left(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    wait(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    wait(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], raa, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    right(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    avancer(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    avancer(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], ral, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    right(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    avancer(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    left(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], rar, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    right(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    avancer(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    right(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], raw, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    right(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    avancer(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    wait(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], rla, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    right(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    left(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    avancer(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], rll, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    right(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    left(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    left(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], rlr, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    right(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    left(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    right(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], rlw, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    right(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    left(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    wait(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], rra, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    right(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    right(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    avancer(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], rrl, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    right(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    right(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    left(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], rrr, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    right(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    right(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    right(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], rrw, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    right(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    right(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    wait(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], rwa, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    right(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    wait(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    avancer(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], rwl, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    right(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    wait(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    left(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], rwr, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    right(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    wait(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    right(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], rww, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    right(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    wait(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    wait(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], waa, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    wait(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    avancer(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    avancer(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], wal, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    wait(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    avancer(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    left(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], war, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    wait(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    avancer(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    right(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], waw, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    wait(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    avancer(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    wait(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], wla, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    wait(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    left(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    avancer(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], wll, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    wait(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    left(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    left(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], wlr, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    wait(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    left(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    right(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], wlw, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    wait(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    left(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    wait(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], wra, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    wait(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    right(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    avancer(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], wrl, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    wait(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    right(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    left(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], wrr, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    wait(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    right(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    right(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], wrw, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    wait(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    right(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    wait(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], wwa, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    wait(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    wait(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    avancer(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], wwl, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    wait(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    wait(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    left(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], wwr, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    wait(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    wait(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    right(D3, [X3, Y3], NewD3, [NewX3, NewY3]).

operateur([X1, Y1, D1, X2, Y2, D2, X3, Y3, D3], www, [NewX1, NewY1, NewD1, NewX2, NewY2, NewD2, NewX3, NewY3, NewD3]) :-
    wait(D1, [X1, Y1], NewD1, [NewX1, NewY1]),
    wait(D2, [X2, Y2], NewD2, [NewX2, NewY2]),
    wait(D3, [X3, Y3], NewD3, [NewX3, NewY3]).


avancer(D, [X, Y], D, [X, Y+1]) :- 
    D == up,
    Y =< 6,
    linked([X, Y], [X, Y+1]).

avancer(D, [X, Y], D, [X-1, Y]) :- 
    D == left,
    X >= 1,
    linked([X, Y], [X-1, Y]).

avancer(D, [X, Y], D, [X+1, Y]) :- 
    D == right,
    X =< 6,
    linked([X, Y], [X+1, Y]).

avancer(D, [X, Y], D, [X, Y-1]) :- 
    D == down,
    Y >= 1,
    linked([X, Y], [X, Y-1]).

left(up, [X, Y], left, [X, Y]) :-
    not(linked([X, Y], [X, Y+1])).

left(left, [X, Y], down, [X, Y]) :-
    not(linked([X, Y], [X-1, Y])).

left(down, [X, Y], right, [X, Y]) :-
    not(linked([X, Y], [X, Y-1])).

left(right, [X, Y], up, [X, Y]) :-
    not(linked([X, Y], [X+1, Y])).

right(up, [X, Y], right, [X, Y]) :-
    not(linked([X, Y], [X, Y+1])).

right(left, [X, Y], up, [X, Y]) :-
    not(linked([X, Y], [X-1, Y])).

right(down, [X, Y], left, [X, Y]) :-
    not(linked([X, Y], [X, Y-1])).

right(right, [X, Y], down, [X, Y]) :-
    not(linked([X, Y], [X+1, Y])).

wait(up, [X, Y], up, [X, Y]) :-
    not(linked([X, Y], [X, Y+1])).

wait(left, [X, Y], left, [X, Y]) :-
    not(linked([X, Y], [X-1, Y])).

wait(down, [X, Y], down, [X, Y]) :-
    not(linked([X, Y], [X, Y-1])).

wait(right, [X, Y], right, [X, Y]) :-
    not(linked([X, Y], [X+1, Y])).

