import os
import module as mm
import tensorflow as tf

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

tf.compat.v1.disable_v2_behavior()
tf.compat.v1.disable_eager_execution()
tf.compat.v1.disable_resource_variables()

class InpaintNN():

    def __init__(self, input_height=256, input_width=256, batch_size=1, bar_model_name=None, bar_checkpoint_name=None, mosaic_model_name=None, mosaic_checkpoint_name=None, is_mosaic=False):
        self.bar_model_name = bar_model_name
        self.bar_checkpoint_name = bar_checkpoint_name
        self.mosaic_model_name = mosaic_model_name
        self.mosaic_checkpoint_name = mosaic_checkpoint_name
        self.is_mosaic = is_mosaic
        self.input_height = input_height
        self.input_width = input_width
        self.batch_size = batch_size
        self.build_model()

    def build_model(self):
        self.X = tf.compat.v1.placeholder(tf.float32, [self.batch_size, self.input_height, self.input_width, 3])
        self.Y = tf.compat.v1.placeholder(tf.float32, [self.batch_size, self.input_height, self.input_width, 3])
        self.MASK = tf.compat.v1.placeholder(tf.float32, [self.batch_size, self.input_height, self.input_width, 3])
        IT = tf.compat.v1.placeholder(tf.float32)

        input = tf.concat([self.X, self.MASK], 3)

        vec_en = mm.encoder(input, reuse=False, name='G_en')

        vec_con = mm.contextual_block(
            vec_en, vec_en, self.MASK, 3, 50.0, 'CB1', stride=1)

        I_co = mm.decoder(vec_en, self.input_height, self.input_height, reuse=False, name='G_de')
        I_ge = mm.decoder(vec_con, self.input_height, self.input_height, reuse=True, name='G_de')

        self.image_result = I_ge * (1-self.MASK) + self.Y*self.MASK

        D_real_red = mm.discriminator_red(self.Y, reuse=False, name='disc_red')
        D_fake_red = mm.discriminator_red(
            self.image_result, reuse=True, name='disc_red')

        # ------- Losses ------- #

        Loss_D_red = tf.reduce_mean(input_tensor=tf.nn.relu(
            1+D_fake_red)) + tf.reduce_mean(input_tensor=tf.nn.relu(1-D_real_red))
        Loss_D = Loss_D_red
        Loss_gan_red = -tf.reduce_mean(input_tensor=D_fake_red)
        Loss_gan = Loss_gan_red
        Loss_s_re = tf.reduce_mean(input_tensor=tf.abs(I_ge - self.Y))
        Loss_hat = tf.reduce_mean(input_tensor=tf.abs(I_co - self.Y))

        A = tf.image.rgb_to_yuv((self.image_result+1)/2.0)
        A_Y = tf.cast(A[:, :, :, 0:1]*255.0, 'int32')

        B = tf.image.rgb_to_yuv((self.Y+1)/2.0)
        B_Y = tf.cast(B[:, :, :, 0:1]*255.0, 'int32')

        ssim = tf.reduce_mean(input_tensor=tf.image.ssim(A_Y, B_Y, 255.0))

        alpha = IT/1000000

        Loss_G = 0.1*Loss_gan + 10*Loss_s_re + 5*(1-alpha) * Loss_hat

        # ------- variable & optimizer ------- #

        var_D = [v for v in tf.compat.v1.global_variables() if v.name.startswith('disc_red')]
        var_G = [v for v in tf.compat.v1.global_variables() if v.name.startswith('G_en') or v.name.startswith('G_de') or v.name.startswith('CB1')]
        update_ops = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.UPDATE_OPS)

        with tf.control_dependencies(update_ops):
            optimize_D = tf.compat.v1.train.AdamOptimizer(learning_rate=0.0004, beta1=0.5, beta2=0.9).minimize(Loss_D, var_list=var_D)
            optimize_G = tf.compat.v1.train.AdamOptimizer(learning_rate=0.0001, beta1=0.5, beta2=0.9).minimize(Loss_G, var_list=var_G)
        config = tf.compat.v1.ConfigProto()
        self.sess = tf.compat.v1.Session(config=config)
        init = tf.compat.v1.global_variables_initializer()
        self.sess.run(init)
        saver = tf.compat.v1.train.Saver()
        if self.is_mosaic:
            Restore = tf.compat.v1.train.import_meta_graph(
                self.mosaic_model_name)
            Restore.restore(self.sess, tf.train.latest_checkpoint(
                self.mosaic_checkpoint_name))
        else:
            Restore = tf.compat.v1.train.import_meta_graph(self.bar_model_name)
            Restore.restore(self.sess, tf.train.latest_checkpoint(self.bar_checkpoint_name))

    def predict(self, censored, unused, mask):
        img_sample = self.sess.run(self.image_result, feed_dict={self.X: censored, self.Y: unused, self.MASK: mask})
        return img_sample
