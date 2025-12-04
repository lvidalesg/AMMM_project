// ** PLEASE ONLY CHANGE THIS FILE WHERE INDICATED **
// In particular, do not change the names of the OPL variables.

int             K = ...;
int 	  P[1..K] = ...;
int 	  R[1..K] = ...;
int 	  A[1..K] = ...;
int 	  C[1..K] = ...;

int             N = ...;
int M[1..N][1..N] = ...;
dvar I[1..2*N];
dvar D[1..7];
dvar boolean x_ik[i in I, k in K];
dvar boolean y_ikd[i in I, k in K, d in D];
dvar int z;
// Define here your decision variables and
// any other auxiliary OPL variables you need.
// You can run an execute block if needed.

//>>>>>>>>>>>>>>>>

//<<<<<<<<<<<<<<<<

// You can run an execute block if needed.

execute {

//>>>>>>>>>>>>>>>>

//<<<<<<<<<<<<<<<<    
}

minimize sum(i in I) sum(k in K) P[k] * x_ik[i,k] + sum(k in K) sum(d in D) C[k] * y_ikd[i,k,d];; // Write here the objective function.


subject to {

// Constraint 1 
forall(i in I)
    sum(k in K) x_ik[i,k] <= 1;
// Constraint 2
forall(k in K) forall(d in D)
    y_ikd[i,k,d] <= x_ik[i,k]
// Constraint 3
forall(d in D)
    y_ikd[i,k,d] >= 1
//Constraint 4
forall(i in I, k in K, d in D)
    sum(t in 0..A[k]) y[i][k][(d+t-1)% 7 + 1] <= A[k];
//Constraint 5
forall(i in I, k in K, d in D) 
    y_ikd[i,k,d] - y_ikd[i,k,(d+5)% 7 + 1] <= y_ikd[i,k,(d%7) + 1];

}

// You can run an execute block if needed.

execute {

//>>>>>>>>>>>>>>>>

//<<<<<<<<<<<<<<<<
}

