import tensorflow as tf
import torch.nn as nn
import torch


def mse_gan_loss(logit_real, logit_fake):
    loss_function = nn.MSELoss()
    target_ones_real = torch.ones_like(logit_real)
    target_ones_fake = torch.ones_like(logit_fake)
    target_zeros = torch.ones_like(logit_fake)

    loss_G = loss_function(logit_fake, target_ones_fake)
    loss_D = loss_function(logit_real, target_ones_real) + loss_function(
        logit_fake, target_zeros)

    return loss_G, loss_D


def gan_loss(logit_real, logit_fake, eps=1e-12):
    g_loss = -tf.reduce_mean(tf.log(logit_fake + eps))
    d_loss = -(tf.reduce_mean(
        tf.log(logit_real + eps) + tf.log(1 - logit_fake + eps)))

    return g_loss, d_loss


def gan_loss_cycle(logit_real, logit_fake):
    # gan loss for cycle gan
    g_loss = tf.reduce_mean((logit_fake - 1)**2)

    d_loss = tf.reduce_mean((logit_real - 1)**2 + logit_fake**2)

    return g_loss, d_loss


def cycle_loss(cycled_A, A, cycled_B, B):
    return tf.reduce_mean(tf.abs(cycled_B - B)) + tf.reduce_mean(
        tf.abs(cycled_A - A))
