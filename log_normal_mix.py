#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__      = "BloomShell"

import numpy as np
from scipy.stats import norm


class LogNormalMixture(object):
    """
    Lognormal-mixture dynamics and calibration to market volatility smiles.
    
    This class implements the model and methods described in the paper:
    "Lognormal-mixture dynamics and calibration to market volatility smiles" 
    by Damiano Brigo, Fabio Mercurio, Francesco Rapisarda.

    From chapter 4: Shifting the overall distribution.
    Quote: "We now show how to construct an even more general model
    by shifting the process (11), while preserving the correct drift.
    Precisely, we assume that the new asset-price process A0 is obtained
    through the following affine transformation of the process S ...".
    """

    @staticmethod
    def sigma_0(
        lambdas: np.ndarray, etas: np.ndarray, tau: float, alpha: float
    ) -> float:
        """
        Calculate the ATM-forward implied volatility (\sigma(0)).

        Parameters:
        lambdas (np.ndarray): Weights of each lognormal distribution.
        etas (np.ndarray): Volatilities standardized by time.
        tau (float): Maturity in years.
        alpha (float): Shift parameter.

        Returns:
        float: The ATM-forward implied volatility.
        """
        return (
            2
            / np.sqrt(tau)
            * norm.ppf(
                (1 - alpha) * np.sum(lambdas * norm.cdf(0.5 * etas * np.sqrt(tau)))
                + 0.5 * alpha
            )
        )

    @staticmethod
    def npv(
        strikes: np.ndarray,
        s0: float,
        mu: float,
        lambdas: np.ndarray,
        etas: np.ndarray,
        tau: float,
        alpha: float,
        flag: int = 1
    ) -> float:
        """
        Calculate the net-present-value of options using the LogNormalMixture model.

        Parameters:
        strikes (np.ndarray): Strike prices.
        s0 (float): Initial asset price.
        mu (float): Drift rate.
        lambdas (np.ndarray): Weights of each lognormal distribution.
        etas (np.ndarray): Volatilities standardized by time.
        tau (float): Maturity in years.
        alpha (float): Shift parameter.
        flag (int): Flag type (1 for call, -1 for put).

        Returns:
        float: The net-present-value of the options.
        """
        k = (strikes.reshape(-1, 1) - s0 * alpha * np.exp(mu * tau))
        a0 = s0 * (1 - alpha)

        d1 = (np.log(a0 / k) + (mu + 0.5 * etas**2) * tau) / (np.sqrt(tau) * etas)
        d2 = (np.log(a0 / k) + (mu - 0.5 * etas**2) * tau) / (np.sqrt(tau) * etas)
        return (
            flag
            * np.exp(-mu * tau)
            * np.sum(
                lambdas
                * (
                    a0 * np.exp(mu * tau) * norm.cdf(flag * d1)
                    - k * norm.cdf(flag * d2)
                ),
                axis=1
            )
        )
    