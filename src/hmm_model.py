"""
Modelo Oculto de Markov (HMM) para Diagnostico y Mantenimiento Predictivo
Implementacion formal para la Actividad de Simulacion - Entrega 2.
Autor: Wilfran Camilo Valencia Goez
"""

import numpy as np
import pandas as pd
from typing import Tuple, List, Dict

class HiddenMarkovModel:
    """
    Especificacion formal de un Modelo Oculto de Markov discreto de primer orden:
    lambda = (A, B, pi)
    donde:
      - S: Conjunto de N estados ocultos {S_0, ..., S_{N-1}}
      - V: Conjunto de M observaciones visibles {V_0, ..., V_{M-1}}
      - A: Matriz de transicion de estados de dimension N x N, donde a_ij = P(q_t = S_j | q_{t-1} = S_i)
      - B: Matriz de emision de observaciones de dimension N x M, donde b_j(k) = P(o_t = V_k | q_t = S_j)
      - pi: Vector de distribucion de estado inicial de dimension N, pi_i = P(q_1 = S_i)
    """

    def __init__(self, states: List[str], observations: List[str], 
                 A: np.ndarray, B: np.ndarray, pi: np.ndarray):
        self.states = states
        self.observations = observations
        self.N = len(states)
        self.M = len(observations)
        
        self.A = np.array(A, dtype=float)
        self.B = np.array(B, dtype=float)
        self.pi = np.array(pi, dtype=float)
        
        # Validaciones estocasticas rigurosas (sumas de filas deben ser 1.0)
        assert self.A.shape == (self.N, self.N), "Dimension de A no coincide con numero de estados"
        assert self.B.shape == (self.N, self.M), "Dimension de B no coincide con estados u observaciones"
        assert len(self.pi) == self.N, "Dimension de pi no coincide con estados"
        assert np.allclose(self.A.sum(axis=1), 1.0), "Las filas de A deben sumar 1"
        assert np.allclose(self.B.sum(axis=1), 1.0), "Las filas de B deben sumar 1"
        assert np.isclose(self.pi.sum(), 1.0), "El vector pi debe sumar 1"

    def simulate(self, T: int, seed: int = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genera una secuencia de T instantes temporales:
          - Secuencia de estados latentes ocultos: Q = (q_1, q_2, ..., q_T)
          - Secuencia de observaciones visibles:   O = (o_1, o_2, ..., o_T)
        """
        if seed is not None:
            np.random.seed(seed)
            
        states_seq = np.zeros(T, dtype=int)
        obs_seq = np.zeros(T, dtype=int)
        
        # Instante t = 0
        states_seq[0] = np.random.choice(self.N, p=self.pi)
        obs_seq[0] = np.random.choice(self.M, p=self.B[states_seq[0]])
        
        # Instantes t = 1 hasta T-1
        for t in range(1, T):
            prev_state = states_seq[t - 1]
            states_seq[t] = np.random.choice(self.N, p=self.A[prev_state])
            obs_seq[t] = np.random.choice(self.M, p=self.B[states_seq[t]])
            
        return states_seq, obs_seq

    def forward(self, obs_seq: np.ndarray) -> Tuple[float, np.ndarray]:
        """
        Problema 1 de HMM: Evaluacion de verosimilitud P(O | lambda) mediante algoritmo Forward.
        Retorna:
          - log_prob: log-verosimilitud
          - alpha: matriz forward de dimension T x N
        """
        T = len(obs_seq)
        alpha = np.zeros((T, self.N), dtype=float)
        
        # Inicializacion
        alpha[0] = self.pi * self.B[:, obs_seq[0]]
        
        # Induccion
        for t in range(1, T):
            for j in range(self.N):
                alpha[t, j] = np.sum(alpha[t - 1] * self.A[:, j]) * self.B[j, obs_seq[t]]
                
        prob_O = np.sum(alpha[T - 1])
        return prob_O, alpha

    def viterbi(self, obs_seq: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Problema 2 de HMM: Decodificacion optima del estado oculto mas probable mediante Viterbi.
        arg max_Q P(Q | O, lambda)
        Retorna:
          - best_path: secuencia optima de estados enteros de longitud T
          - best_prob: probabilidad de la trayectoria mas verosimil
        """
        T = len(obs_seq)
        delta = np.zeros((T, self.N), dtype=float)
        psi = np.zeros((T, self.N), dtype=int)
        
        # Inicializacion (en escala logaritmica para evitar subdesbordamiento numerico)
        small_eps = 1e-12
        log_pi = np.log(self.pi + small_eps)
        log_A = np.log(self.A + small_eps)
        log_B = np.log(self.B + small_eps)
        
        delta[0] = log_pi + log_B[:, obs_seq[0]]
        psi[0] = 0
        
        # Recursion
        for t in range(1, T):
            for j in range(self.N):
                temp = delta[t - 1] + log_A[:, j]
                psi[t, j] = np.argmax(temp)
                delta[t, j] = np.max(temp) + log_B[j, obs_seq[t]]
                
        # Terminacion y Backtracking
        best_path = np.zeros(T, dtype=int)
        best_path[T - 1] = np.argmax(delta[T - 1])
        best_log_prob = np.max(delta[T - 1])
        
        for t in range(T - 2, -1, -1):
            best_path[t] = psi[t + 1, best_path[t + 1]]
            
        return best_path, best_log_prob

    def compute_accuracy(self, true_states: np.ndarray, decoded_states: np.ndarray) -> float:
        """Calcula la exactitud (accuracy) de la decodificacion de Viterbi frente al estado real."""
        return float(np.mean(true_states == decoded_states))
