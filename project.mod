// ** PLEASE ONLY CHANGE THIS FILE WHERE INDICATED **
// In particular, do not change the names of the OPL variables.

int             K = ...;
int 	  P[1..K] = ...;
int 	  R[1..K] = ...;
int 	  A[1..K] = ...;
int 	  C[1..K] = ...;

int             N = ...;
int M[1..N][1..N] = ...;
//dvar int I[1..N];
range I = 1..N;
range Ka = 1..K;
range D = 1..7;
//dvar int D[1..7];
dvar boolean x_ik[i in I, k in Ka];
dvar boolean y_ikd[i in I, k in Ka, d in D];
dvar int z;

// Set CPLEX parameter for 1% optimality gap
execute {
  cplex.epgap = 0.01;
  cplex.tilim = 1800;
}

minimize (sum(i in I) sum(k in Ka) P[k] * x_ik[i,k]) + (sum(i in I) sum(k in Ka) sum(d in D) C[k] * y_ikd[i,k,d]); // Write here the objective function.


subject to {

// Constraint 1 
forall(i in I)
    sum(k in Ka) x_ik[i,k] <= 1;
// Constraint 2
forall(i in I) forall(k in Ka) forall(d in D)
    y_ikd[i,k,d] <= x_ik[i,k];
// Constraint 3
forall(j in I, d in D)
    sum(i in I, k in Ka : R[k] >= M[i][j]) y_ikd[i,k,d] >= 1;
//Constraint 4
forall(i in I, k in Ka, d in D)
    sum(t in 0..A[k]) y_ikd[i,k,(d+t-1)% 7 + 1] <= A[k];
//Constraint 5
forall(i in I, k in Ka, d in D) 
    y_ikd[i,k,d] - y_ikd[i,k,(d+6-1)% 7 + 1] <= y_ikd[i,k,(d%7) + 1];

}

// You can run an execute block if needed.

execute {

//>>>>>>>>>>>>>>>>

//<<<<<<<<<<<<<<<<
}

