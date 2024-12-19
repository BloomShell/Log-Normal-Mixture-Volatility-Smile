# lognormal-mixture

This project implements the LogNormal-mixture model for option pricing, based on the paper *"Lognormal-mixture dynamics and calibration to market volatility smiles"* by Damiano Brigo, Fabio Mercurio, and Francesco Rapisarda. The model and methods are encapsulated in a Python class and are used to calculate implied volatilities and option prices.

## Introduction

The LogNormalMixture model is used to fit market volatility smiles by modeling the underlying asset price as a mixture of lognormal distributions. This project provides the tools to calculate the net-present-value (NPV) of options and their implied volatilities using this model.

## Visualize the model implied volatilities

<p align="center">
    <img src="https://i.imgur.com/Vpwt0ru.png" width="900"/>
</p>

## Mixtures of distributions

Reading Piterbarg's paper *"Mixture of Models: A Simple Recipe for a ... Hangover?"*. Starting from the idea of using a weighted average of derivative security prices computed using different “simple” models (the so-called “mixture of models” or “ensemble of models” approach) as a simple way to add stochastic volatility to virtually any model. Perhaps, the mixture of normal distributions (i.e., a distribution with a density that is a weighted average of two or more Gaussian densities with different volatilities) has heavy tails.

To use a mixture model to price path-dependent products, one must specify the mixture model dynamics, particularly how probabilities (weights) of different volatility scenarios evolve over time. This is done in the lognormal mixture model (Brigo and Mercurio), where the risk-neutral density of the asset is a mixture of lognormal densities, and an analytical diffusion coefficient is specified. The square of the local volatility \( \nu(t, y) \) is a weighted average of the squared basic volatilities \( \sigma_1^2(t), \dots, \sigma_N^2(t) \), with weights as functions of the marginal lognormal densities:

\begin{align*}
\nu^2(t, y) = \sum_{i=1}^N \Lambda_i(t, y) \sigma_i^2(t) = \frac{\sum_{i=1}^N \lambda_i \sigma_i^2 p_i(S)}{\sum_{i=1}^N \lambda_i p_i(S)}.
\end{align*}

In the example provided, the probabilities (weights) of the volatility scenarios remain constant over time. The basic interpretation of defining the mixture model with the above static approach assumes the weights are fixed from time \( t_0 \) all the way to the final maturity \( T \). However, this uncertainty is *"resolved in the next millisecond"*, but the non-dynamic stochastic volatility model only specifies what is going to happen to those volatility scenarios at a fixed time in the future, and not what happens in between now (\( t_0 \)) and then (\( T \)). This static approach, where the value of the derivative in the mixture model is given by:
$$
\displaystyle
\left( \sum_{k=1}^n a_k b_k \right)^2
\leq
\left( \sum_{k=1}^n a_k^2 \right)
\left( \sum_{k=1}^n b_k^2 \right)
$$
\[
V_{\text{MM}} = \sum_{i=1}^N p_i V(S_i),
\]

is unsuitable for valuing path-dependent derivatives, as it does not account for how volatility uncertainty evolves. While this works for simple contracts like European options (the actual volatility path has no bearing on the option value, as only the average volatility, *terminal distribution*, between now and the option’s expiry matters), it fails for contracts requiring an understanding of underlying market dynamics.

For instance, the example considers a simple compound option. Using the mixture model, its value computed as a *direct valuation approach* is:

\[
V_{\text{MM}}(0, S_0) = p_1 \mathbb{E}_1 \left[ \max \left( K_1 - S_{T_1}, \mathbb{E}_1^{T_1} \left[ (K_2 - S_{T_2})^+ \right] \right) \right] 
+ p_2 \mathbb{E}_2 \left[ \max \left( K_1 - S_{T_1}, \mathbb{E}_2^{T_1} \left[ (K_2 - S_{T_2})^+ \right] \right) \right].
\]

Path-dependent options, such as the compound option in the example, depend on the path between now and maturity. The *continuation value approach*, \( \tilde{V}_{MM} \), looks at the value at \( T_1 \) and then discounts it back—still using the *same fixed weights* when computing the expected value at \( T_1 \), refusing to account for how the probability of being in a particular volatility regime may have *changed* by \( T_1 \), depending on the path taken by the underlying asset. At \( T_1 \), the compound option value is:

\[
V_{\text{MM}}(T_1, S) = \mathbb{1}_{\{S > S^*\}} H(S) + \mathbb{1}_{\{S \leq S^*\}} (K_1 - S),
\]

where:

\[
H(S) = p_1 \mathbb{E}_1^{T_1} \left[ (K_2 - S_{T_2})^+ \mid S_{T_1} = S \right] 
+ p_2 \mathbb{E}_2^{T_1} \left[ (K_2 - S_{T_2})^+ \mid S_{T_1} = S \right].
\]

The continuation value at \( t_0 \) is given by:

\[
\tilde{V}_{\text{MM}}(0, S_0) = p_1 \mathbb{E}_1 \left[ V_{\text{MM}}(T_1, S_{T_1}) \right] + 
p_2 \mathbb{E}_2 \left[ V_{\text{MM}}(T_1, S_{T_1}) \right].
\]

However, these two valuations are inconsistent:

\[
V_{\text{MM}}(0, S_0) \neq \tilde{V}_{\text{MM}}(0, S_0).
\]

This inconsistency arises because the mixture model fails to account for the dynamics of volatility uncertainty.

## References

- Brigo, D., Mercurio, F., & Rapisarda, F. (Year). *Lognormal-mixture dynamics and calibration to market volatility smiles.* Retrieved from [Imperial College](https://www.ma.imperial.ac.uk/~dbrigo/lognsmile.pdf)
- Piterbarg, V. *Mixture of Models: A Simple Recipe for a ... Hangover?* ([SSRN](https://ssrn.com/abstract=393060))
