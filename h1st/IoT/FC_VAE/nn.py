import abc
import math
import json
import os
import pprint
import sys
import shutil

# import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

import scipy.stats
import numpy as np

# from h1st.dl.util.logger import logger


import tensorflow_probability as tfp
tfd = tfp.distributions


layers = tf.keras.layers

_NAME_SCOPE = "h1st"



def l1_l2_regularizer(scale_l1=1.0, scale_l2=1.0, scope=None):
  """Returns a function that can be used to apply L1 L2 regularizations.
  
  Args:
    scale_l1: A scalar multiplier `Tensor` for L1 regularization.
    scale_l2: A scalar multiplier `Tensor` for L2 regularization.
    scope: An optional scope name.
  
  Returns:
    A function with signature `l1_l2(weights)` that applies a weighted sum of
    L1 L2  regularization.
  
  Raises:
    ValueError: If scale is negative or if scale is not a float.

  Backport from TF master branch.
  """
  scope = scope or 'l1_l2_regularizer'
  return tf.contrib.layers.sum_regularizer([tf.contrib.layers.l1_regularizer(scale_l1),
                                            tf.contrib.layers.l2_regularizer(scale_l2)],
                                           scope=scope)


class _Dense_BN(tf.keras.Model):
  def __init__(self, networks, base_name):
      super(_Dense_BN, self).__init__()
      self.networks_list = []
      for idx, layer in enumerate(networks):
          self.dense = layers.Dense(
              layer, kernel_initializer="glorot_uniform", name=base_name+"_dense"+str(idx))
          self.networks_list.append(self.dense)
          self.bn = layers.BatchNormalization(name=base_name+"_bn"+ str(idx))
          self.networks_list.append(self.bn)
 
    
       
    

  def call(self, input_tensor, training=False):
      x = self.networks_list[0](input_tensor)
      x = self.networks_list[1](x, training=training)
      x = tf.nn.tanh(x)
      for i in range(2, len(self.networks_list), 2):
          x = self.networks_list[i](x)
          x = self.networks_list[i+1](x, training=training)
          x = tf.nn.tanh(x) # tf.nn.elu(x)
      return x


class _Dense(tf.keras.Model):
  def __init__(self, networks, base_name):
      super(_Dense, self).__init__()
      self.networks_list = []
      for idx, layer in enumerate(networks):
          self.dense = layers.Dense(
              layer, kernel_initializer="glorot_uniform", name=base_name+"_dense"+str(idx))
          self.networks_list.append(self.dense)


  def call(self, input_tensor, training=False):
      x = self.networks_list[0](input_tensor)
      x = tf.nn.tanh(x)
      for i in range(1, len(self.networks_list)):
          x = self.networks_list[i](x)
          x = tf.nn.tanh(x) # tf.nn.elu(x)
      return x


class VAE(tf.keras.Model):
  def __init__(self, encoding_networks, decoding_networks, n_input, n_z, n_rank=0, bn=False, alpha=0, drop_rate=0.0):
    super(VAE, self).__init__(name="vae")
    
    self.alpha = alpha
    self.drop_rate = drop_rate
    self.n_input = n_input
    self.n_rank = n_rank

    if bn:
        self.encoder = _Dense_BN(encoding_networks, "encoder")
    else:
        self.encoder = _Dense(encoding_networks, "encoder")
    self.get_z_mean = layers.Dense(
        n_z, kernel_initializer="glorot_uniform", name="z_mean")  
    self.get_z_logvar = layers.Dense(
        n_z, kernel_initializer="glorot_uniform", name="z_sigma")
    self.z_prior_pdf = tfd.MultivariateNormalDiag(tf.zeros(n_z), tf.ones(n_z))

    if bn:
        self.decoder = _Dense_BN(decoding_networks, "decoder")
    else:
        self.decoder = _Dense(decoding_networks, "decoder")
    self.get_x_mean = layers.Dense(
        self.n_input, kernel_initializer="glorot_uniform", name="x_mean")  
    self.get_x_logvar = layers.Dense(
        self.n_input, kernel_initializer="glorot_uniform", name="x_sigma")

    self.dropout_encoder = layers.Dropout(rate=self.drop_rate)
    self.dropout_decoder = layers.Dropout(rate=self.drop_rate)

    # LowRank Approximation
    if self.n_rank:
      self.get_scale_perturb_factor = layers.Dense(
        n_input*n_rank, kernel_initializer="glorot_uniform", name="get_scale_perturb_factor")
      self.get_scale_perturb_diag = layers.Dense(
        n_rank, kernel_initializer="glorot_uniform", name="get_scale_perturb_diag")      


  def call(self, input_tensor, num_sample, training=False):
    z_post_pdf = self.get_z_post_pdf(input_tensor, training=training)
    log_prob_list = []
    for _ in range(num_sample):     
      z_sample = z_post_pdf.sample()
      # epsilon = self.z_prior_pdf.sample()
      # z_sample = z_mean + z_sigma * epsilon
      x_pdf = self.get_x_pdf(z_sample, training=training)
      x_log_prob = x_pdf.log_prob(input_tensor)
      log_prob_list.append(x_log_prob)
    log_prob_vector = tf.stack(log_prob_list)
    return tf.reduce_mean(log_prob_vector, axis=0)        


  def get_z_param(self, input_tensor, training=False):
    temp = self.encoder(input_tensor, training=training)
    dropout = self.dropout_encoder(temp, training=training)
    z_mean = self.get_z_mean(dropout)
    z_logvar = self.get_z_logvar(dropout)
    return [z_mean, z_logvar]


  def get_z_post_pdf(self, input_tensor, training=False):
    z_mean, z_logvar = self.get_z_param(input_tensor, training=training)
    z_sigma = tf.sqrt(tf.exp(z_logvar))
    z_post_pdf = tfd.MultivariateNormalDiag(z_mean, z_sigma)     
    return z_post_pdf    


  def get_x_param_from_z(self, z_sample, training=False):
    temp = self.decoder(z_sample, training=training)
    dropout = self.dropout_decoder(temp, training=training)     
    x_mean = self.get_x_mean(dropout)
    x_logvar = self.get_x_logvar(dropout)
    return [x_mean, x_logvar]


  def get_x_pdf(self, z_sample, training=False):
    temp = self.decoder(z_sample, training=training)
    dropout = self.dropout_decoder(temp, training=training)     
    x_mean = self.get_x_mean(dropout)
    x_logvar = self.get_x_logvar(dropout)
    x_sigma = tf.sqrt(tf.exp(x_logvar))

    if self.n_rank:
      m_scale = tf.nn.softplus(self.get_scale_perturb_diag(dropout)) + 1e-10
      u_scale = tf.nn.softplus(self.get_scale_perturb_factor(dropout)) + 1e-10        
      u_scale = tf.reshape(u_scale, shape=[-1, self.n_input, self.n_rank])
      x_pdf = tfd.MultivariateNormalDiagPlusLowRank(
          loc=x_mean,
          scale_diag=x_sigma+self.alpha,
          scale_perturb_factor=u_scale,
          scale_perturb_diag=m_scale)         
    else:
      x_pdf = tfd.MultivariateNormalDiag(x_mean, x_sigma+self.alpha)

    return x_pdf


  def get_x_sigma(self, z_sample, training=False):
    temp = self.decoder(z_sample, training=training)
    dropout = self.dropout_decoder(temp, training=training)
    x_logvar = self.get_x_logvar(dropout)
    x_sigma = tf.sqrt(tf.exp(x_logvar))    
    m_scale = tf.nn.softplus(self.get_scale_perturb_diag(dropout)) + 1e-10
    u_scale = tf.nn.softplus(self.get_scale_perturb_factor(dropout)) + 1e-10        
    u_scale = tf.reshape(u_scale, shape=[-1, self.n_input, self.n_rank])
    final_sigma = x_sigma + tf.linalg.diag_part(tf.matmul(tf.matmul(
                                  u_scale, 
                                  tf.linalg.diag(m_scale)), 
                                  tf.linalg.transpose(u_scale)))
    return final_sigma


  def get_prob_for_individual_sensor(self, input_tensor, num_sensors, num_sample, window_size=1, training=False):
    prob_for_each_sensor_list = []
    z_post_pdf = self.get_z_post_pdf(input_tensor, training=training)
    for _ in range(num_sample):
      # epsilon = self.z_prior_pdf.sample()
      # z_sample = z_mean + z_sigma * epsilon
      z_sample = z_post_pdf.sample()
      x_mean, x_logvar = self.get_x_param_from_z(z_sample, training=training)
      if self.n_rank:
        x_sigma = self.get_x_sigma(z_sample, training=training)
      else:
        x_sigma = tf.sqrt(tf.exp(x_logvar))
      normal_dist = tf.distributions.Normal(loc=x_mean, scale=x_sigma)
      prob_for_each_sensor = normal_dist.prob(input_tensor)
      prob_for_each_sensor_list.append(prob_for_each_sensor)
    prob_for_each_sensor_vector = tf.stack(prob_for_each_sensor_list)    
    prob_for_each_sensor_final = tf.reduce_mean(prob_for_each_sensor_vector, axis=0) 
    if window_size > 1:
      reshaped_prob = tf.reshape(prob_for_each_sensor_final, [-1, window_size, num_sensors])
      prob_for_each_sensor_final = tf.reduce_mean(reshaped_prob, axis=[1])
    return prob_for_each_sensor_final    


  def get_analytic_loss_n_mae(self, input_tensor, beta=1, training=True):
    def log_likelihood(input_val, mean, logvar, raxis=1):
      log2pi = tf.log(2. * np.pi)
      return tf.reduce_sum(
        -.5 * ((input_val - mean) ** 2. * tf.exp(-logvar) + logvar + log2pi),
        axis=raxis)

    def kl_divergence(mean, logvar, raxis=1):
      return tf.reduce_sum(
        .5 * (mean ** 2. + tf.exp(logvar) - logvar - 1),
        axis=raxis)

    # Get loss
    z_post_pdf = self.get_z_post_pdf(input_tensor, training=training)
    z_sample = z_post_pdf.sample()
    # epsilon = self.z_prior_pdf.sample()
    # z_sample = z_mean + z_sigma * epsilon
    x_mean, x_logvar = self.get_x_param_from_z(z_sample, training=training)
    ELBO = log_likelihood(input_tensor, x_mean, x_logvar) \
            - beta*kl_divergence(z_mean, z_logvar)
    loss = tf.reduce_mean(-ELBO)

    # Get MAE
    mae, mae_update_op = tf.metrics.mean_absolute_error(input_tensor, x_mean)

    return [loss, mae, mae_update_op] 


  def get_mc_loss_n_mae(self, input_tensor, beta=1, training=True):
    # Get loss
    z_post_pdf = self.get_z_post_pdf(input_tensor, training=training)
    z_sample = z_post_pdf.sample()
    # epsilon = self.z_prior_pdf.sample()
    # z_sample = z_mean + z_sigma * epsilon
    x_mean, _ = self.get_x_param_from_z(z_sample, training=training)
    x_pdf = self.get_x_pdf(z_sample, training=training)
    x_log_prob = x_pdf.log_prob(input_tensor)
    ELBO = x_log_prob - beta*(z_post_pdf.log_prob(z_sample) - \
                              self.z_prior_pdf.log_prob(z_sample))
    loss = tf.reduce_mean(-ELBO)

    # Get MAE
    mae, mae_update_op = tf.metrics.mean_absolute_error(input_tensor, x_mean, name="my_mae")

    return [loss, mae, mae_update_op]
