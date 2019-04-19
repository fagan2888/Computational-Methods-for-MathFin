# -*- coding: utf-8 -*-

# MF 796 - Assignment 1, Problem 5
# Lingyi Xu, U77017242
# Date: 2019-01-26


import numpy as np
import scipy.stats as sc
import math


# (b) European call price by simulation
def stock_price_simu(S0,r,sigma,beta,t,N,n): 
    # dSt = r * St * dt + sigma * St^beta * dWt
    # N denotes # of simulations, n denotes # of periods
    
    # St_list stores the terminal value of a simulation
    St_list = np.empty(N)
    
    # dt denotes the length of each period
    dt = t/n
    
    # set initial value for St
    St = S0
    
    for i in range(N):
        dWt = np.random.normal(loc = 0, scale = math.sqrt(dt), size = n)
        dSt = r*St*dt + sigma*(St**beta)*dWt
        St = S0 + sum(dSt)
        St_list[i] = St
    
    stock_mean = np.mean(St_list)
    stock_var = np.var(St_list)
    
    return St_list, stock_mean, stock_var


def eu_call_price(S0,K,r,sigma,beta,t,N,n):
    # this function calculates the European call price based on simulation
    
    stock_ter_value, _, _ = stock_price_simu(S0,r,sigma,beta,t,N,n)
    stock_ter_value = np.array(stock_ter_value)
    payoff = stock_ter_value - K
    payoff[payoff < 0] = 0
    call_mean = np.mean(payoff)
    call_std = np.std(payoff)
    
    return payoff, call_mean, call_std


S0 = 100
r = 0.0
beta = 1.0
sigma = 0.25
K = S0   # at-the-money

t = 1
N = 10000
n = 10000

_, price, _ = eu_call_price(S0,K,r,sigma,beta,t,N,n)


# (c) European call price by BS model
def bs_price(r,sigma,T,S0,K):
    # calculate the option price via Black-Scholes Formula
    
    d1 = 1.0/(sigma*np.sqrt(T))*(np.log(S0/K)+(r+.5*(sigma**2))*T)
    d2 = d1 - sigma*np.sqrt(T)
    BS_price = S0*sc.norm.cdf(d1) - math.exp(-r*T)*K*sc.norm.cdf(d2)
    
    return BS_price, d1, d2

BS_price, d1, d2 = bs_price(r,sigma,t,S0,K)


# (d) option delta
delta = sc.norm.cdf(d1)


# (e) short position in stocks
share = delta

# (f) portfolio value
def port_val_simu(S0,K,r,sigma,beta,delta,t,N,n):
    
    St_list = np.empty(N)
    dt = t/n
    St = S0
    
    for i in range(N):
        dWt = np.random.normal(loc = 0, scale = math.sqrt(dt), size = n)
        dSt = r*St*dt + sigma*(St**beta)*dWt
        St = S0 + sum(dSt)
        St_list[i] = St
    
    port_val_list = np.maximum(St_list-K, 0)-(St_list-S0)
    
    return port_val_list.mean()

port_val = port_val_simu(S0,K,r,sigma,beta,delta,t,N,n)


# (g) beta value change
beta_new = 0.5
port_val_1 = port_val_simu(S0,K,r,sigma,beta_new,delta,t,N,n)


# (h) sigma value change
sigma_new = 0.4
d1_new = 1.0/(sigma_new*np.sqrt(t))*(np.log(S0/K)+(r+.5*(sigma_new**2))*t)
delta_new = sc.norm.cdf(d1_new)
port_val_2 = port_val_simu(S0,K,r,sigma_new,beta,delta,t,N,n)
