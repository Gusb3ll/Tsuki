import math
from ops import *

def conv_nn(input, dims1, dims2, size1, size2, k_size=3):
    pp = tf.pad(tensor=input, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]], mode="REFLECT")
    L1 = layers.conv2d(pp, dims1, [k_size, k_size], stride=[1, 1], padding='VALID', activation_fn=None)
    L1 = tf.nn.elu(L1)
    pp = tf.pad(tensor=L1, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]], mode="REFLECT")
    L2 = layers.conv2d(pp, dims2, [k_size, k_size], stride=[1, 1], padding='VALID', activation_fn=None)
    L2 = tf.nn.elu(L2)
    L2 = tf.compat.v1.image.resize_nearest_neighbor(L2, (size1, size2))
    return L2

def encoder(input, reuse, name):
    with tf.compat.v1.variable_scope(name):
        if reuse:
            tf.compat.v1.get_variable_scope().reuse_variables()
        else:
            assert tf.compat.v1.get_variable_scope().reuse is False
        p = tf.pad(tensor=input, paddings=[[0, 0], [2, 2], [2, 2], [0, 0]], mode="REFLECT")
        CL1 = layers.conv2d(p, 32, [5, 5], stride=[1, 1], padding='VALID', activation_fn=None)
        CL1 = tf.nn.elu(CL1)  # 256 256 32
        p = tf.pad(tensor=CL1, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]], mode="REFLECT")
        CL2 = layers.conv2d(p, 64, [3, 3], stride=[2, 2], padding='VALID', activation_fn=None)
        CL2 = tf.nn.elu(CL2)  # 128 128 64
        p = tf.pad(tensor=CL2, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]], mode="REFLECT")
        CL3 = layers.conv2d(p, 64, [3, 3], stride=[1, 1], padding='VALID', activation_fn=None)
        CL3 = tf.nn.elu(CL3)  # 128 128 64
        p = tf.pad(tensor=CL3, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]], mode="REFLECT")
        CL4 = layers.conv2d(p, 128, [3, 3], stride=[2, 2], padding='VALID', activation_fn=None)
        CL4 = tf.nn.elu(CL4)  # 64 64 128
        p = tf.pad(tensor=CL4, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]], mode="REFLECT")
        CL5 = layers.conv2d(p, 128, [3, 3], stride=[1, 1], padding='VALID', activation_fn=None)
        CL5 = tf.nn.elu(CL5)  # 64 64 128
        p = tf.pad(tensor=CL5, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]], mode="REFLECT")
        CL6 = layers.conv2d(p, 256, [3, 3], stride=[2, 2], padding='VALID', activation_fn=None)
        CL6 = tf.nn.elu(CL6)  # 32 32 128
        p = tf.pad(tensor=CL6, paddings=[[0, 0], [2, 2], [2, 2], [0, 0]], mode="REFLECT")
        DCL1 = layers.conv2d(p, 256, [3, 3], rate=2, stride=[1, 1], padding='VALID', activation_fn=None)
        DCL1 = tf.nn.elu(DCL1)
        p = tf.pad(tensor=DCL1, paddings=[[0, 0], [4, 4], [4, 4], [0, 0]], mode="REFLECT")
        DCL2 = layers.conv2d(p, 256, [3, 3], rate=4, stride=[1, 1], padding='VALID', activation_fn=None)
        DCL2 = tf.nn.elu(DCL2)
        p = tf.pad(tensor=DCL2, paddings=[[0, 0], [8, 8], [8, 8], [0, 0]], mode="REFLECT")
        DCL3 = layers.conv2d(p, 256, [3, 3], rate=8, stride=[1, 1], padding='VALID', activation_fn=None)
        DCL3 = tf.nn.elu(DCL3)
        p = tf.pad(tensor=DCL3, paddings=[[0, 0], [16, 16], [16, 16], [0, 0]], mode="REFLECT")
        DCL4 = layers.conv2d(p, 256, [3, 3], rate=16, stride=[1, 1], padding='VALID', activation_fn=None)
        DCL4 = tf.nn.elu(DCL4)  # 32 32 128
        return DCL4

def decoder(input, size1, size2, reuse, name):
    with tf.compat.v1.variable_scope(name):
        if reuse:
            tf.compat.v1.get_variable_scope().reuse_variables()
        else:
            assert tf.compat.v1.get_variable_scope().reuse is False
        DL1 = conv_nn(input, 128, 128, int(size1/4), int(size2/4))
        DL2 = conv_nn(DL1, 64, 64, int(size1/2), int(size2/2))
        DL3 = conv_nn(DL2, 32, 32, int(size1), int(size2))
        DL4 = conv_nn(DL3, 16, 16, int(size1), int(size2))
        LL2 = layers.conv2d(DL4, 3, [3, 3], stride=[1, 1], padding='SAME', activation_fn=None)  # 256 256 3
        LL2 = tf.clip_by_value(LL2, -1.0, 1.0)
        return LL2

def discriminator_G(input, reuse, name):
    with tf.compat.v1.variable_scope(name):
        if reuse:
            tf.compat.v1.get_variable_scope().reuse_variables()
        else:
            assert tf.compat.v1.get_variable_scope().reuse is False
        p = tf.pad(tensor=input, paddings=[[0, 0], [2, 2], [2, 2], [0, 0]], mode="REFLECT")
        L1 = layers.conv2d(p, 64, [5, 5], stride=2, padding='VALID', activation_fn=None)
        L1 = tf.nn.leaky_relu(L1)
        p = tf.pad(tensor=L1, paddings=[[0, 0], [2, 2], [2, 2], [0, 0]], mode="REFLECT")
        L2 = layers.conv2d(p, 128, [5, 5], stride=2, padding='VALID', activation_fn=None)
        L2 = tf.nn.leaky_relu(L2)
        p = tf.pad(tensor=L2, paddings=[[0, 0], [2, 2], [2, 2], [0, 0]], mode="REFLECT")
        L3 = layers.conv2d(p, 256, [5, 5], stride=2, padding='VALID', activation_fn=None)
        L3 = tf.nn.leaky_relu(L3)
        p = tf.pad(tensor=L3, paddings=[[0, 0], [2, 2], [2, 2], [0, 0]], mode="REFLECT")
        L4 = layers.conv2d(p, 256, [5, 5], stride=2, padding='VALID', activation_fn=None)
        L4 = tf.nn.leaky_relu(L4)
        L4 = layers.flatten(L4)
        L5 = tf.compat.v1.layers.dense(L4, 1)
        return L5

def discriminator_L(input, reuse, name):
    with tf.compat.v1.variable_scope(name):
        if reuse:
            tf.compat.v1.get_variable_scope().reuse_variables()
        else:
            assert tf.compat.v1.get_variable_scope().reuse is False
        p = tf.pad(tensor=input, paddings=[[0, 0], [2, 2], [2, 2], [0, 0]], mode="REFLECT")
        L1 = layers.conv2d(p, 64, [5, 5], stride=2, padding='VALID', activation_fn=None)
        L1 = tf.nn.leaky_relu(L1)  # 32 32 64
        p = tf.pad(tensor=L1, paddings=[[0, 0], [2, 2], [2, 2], [0, 0]], mode="REFLECT")
        L2 = layers.conv2d(p, 128, [5, 5], stride=2, padding='VALID', activation_fn=None)
        L2 = tf.nn.leaky_relu(L2)  # 16 16 128
        p = tf.pad(tensor=L2, paddings=[[0, 0], [2, 2], [2, 2], [0, 0]], mode="REFLECT")
        L3 = layers.conv2d(p, 256, [5, 5], stride=2, padding='VALID', activation_fn=None)
        L3 = tf.nn.leaky_relu(L3)  # 8 8 256
        p = tf.pad(tensor=L3, paddings=[[0, 0], [2, 2], [2, 2], [0, 0]], mode="REFLECT")
        L4 = layers.conv2d(p, 512, [5, 5], stride=2, padding='VALID', activation_fn=None)
        L4 = tf.nn.leaky_relu(L4)  # 4 4 512
        L4 = layers.flatten(L4)
        L5 = tf.compat.v1.layers.dense(L4, 1)
        return L5

def discriminator_red(input, reuse, name):
    with tf.compat.v1.variable_scope(name):
        if reuse:
            tf.compat.v1.get_variable_scope().reuse_variables()
        else:
            assert tf.compat.v1.get_variable_scope().reuse is False
        L1 = convolution_SN(input, 64, 5, 2, 'l1')
        L1 = tf.nn.leaky_relu(L1)
        L2 = convolution_SN(L1, 128, 5, 2, 'l2')
        L2 = tf.nn.leaky_relu(L2)
        L3 = convolution_SN(L2, 256, 5, 2, 'l3')
        L3 = tf.nn.leaky_relu(L3)
        L4 = convolution_SN(L3, 256, 5, 2, 'l4')
        L4 = tf.nn.leaky_relu(L4)
        L5 = convolution_SN(L4, 256, 5, 2, 'l5')
        L5 = tf.nn.leaky_relu(L5)
        L6 = convolution_SN(L5, 512, 5, 2, 'l6')
        L6 = tf.nn.leaky_relu(L6)
        L7 = dense_RED_SN(L6, 'l7')
        return L7

def contextual_block(bg_in, fg_in, mask, k_size, lamda, name, stride=1):
    with tf.compat.v1.variable_scope(name):
        b, h, w, dims = [i.value for i in bg_in.get_shape()]
        temp = tf.compat.v1.image.resize_nearest_neighbor(mask, (h, w))
        temp = tf.expand_dims(temp[:, :, :, 0], 3)
        mask_r = tf.tile(temp, [1, 1, 1, dims])
        bg = bg_in * mask_r
        kn = int((k_size - 1) / 2)
        c = 0

        for p in range(kn, h - kn, stride):
            for q in range(kn, w - kn, stride):
                c += 1

        patch1 = tf.compat.v1.extract_image_patches(bg, [1, k_size, k_size, 1], [1, stride, stride, 1], [1, 1, 1, 1], 'VALID')
        patch1 = tf.reshape(patch1, (b, 1, c, k_size*k_size*dims))
        patch1 = tf.reshape(patch1, (b, 1, 1, c, k_size * k_size * dims))
        patch1 = tf.transpose(a=patch1, perm=[0, 1, 2, 4, 3])
        patch2 = tf.compat.v1.extract_image_patches(fg_in, [1, k_size, k_size, 1], [1, 1, 1, 1], [1, 1, 1, 1], 'SAME')

        ACL = []

        for ib in range(b):
            k1 = patch1[ib, :, :, :, :]
            k1d = tf.reduce_sum(input_tensor=tf.square(k1), axis=2)
            k2 = tf.reshape(k1, (k_size, k_size, dims, c))
            ww = patch2[ib, :, :, :]
            wwd = tf.reduce_sum(input_tensor=tf.square(ww), axis=2, keepdims=True)
            ft = tf.expand_dims(ww, 0)
            CS = tf.nn.conv2d(input=ft, filters=k1, strides=[1, 1, 1, 1], padding='SAME')
            tt = k1d + wwd

            DS1 = tf.expand_dims(tt, 0) - 2 * CS
            DS2 = (DS1 - tf.reduce_mean(input_tensor=DS1, axis=3, keepdims=True)) / reduce_std(DS1, 3, True)
            DS2 = -1 * tf.nn.tanh(DS2)
            CA = softmax(lamda * DS2)
            ACLt = tf.nn.conv2d_transpose(CA, k2, output_shape=[1, h, w, dims], strides=[1, 1, 1, 1], padding='SAME')
            ACLt = ACLt / (k_size ** 2)
            if ib == 0:
                ACL = ACLt
            else:
                ACL = tf.concat((ACL, ACLt), 0)
        ACL = bg + ACL * (1.0 - mask_r)
        con1 = tf.concat([bg_in, ACL], 3)
        ACL2 = layers.conv2d(con1, dims, [1, 1], stride=[1, 1], padding='VALID', activation_fn=None, scope='ML')
        ACL2 = tf.nn.elu(ACL2)
        return ACL2

def contextual_block_cs(bg_in, fg_in, mask, k_size, lamda, name, stride=1):
    with tf.compat.v1.variable_scope(name):
        b, h, w, dims = [i.value for i in bg_in.get_shape()]
        temp = tf.image.resize(mask, (h, w), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
        temp = tf.expand_dims(temp[:, :, :, 0], 3)  # b 128 128 1
        mask_r = tf.tile(temp, [1, 1, 1, dims])  # b 128 128 128
        bg = bg_in * mask_r
        kn = int((k_size - 1) / 2)
        c = 0

        for p in range(kn, h - kn, stride):
            for q in range(kn, w - kn, stride):
                c += 1

        patch1 = tf.compat.v1.extract_image_patches(bg, [1, k_size, k_size, 1], [1, stride, stride, 1], [1, 1, 1, 1], 'VALID')
        patch1 = tf.reshape(patch1, (b, 1, c, k_size*k_size*dims))
        patch1 = tf.reshape(patch1, (b, 1, 1, c, k_size * k_size * dims))
        patch1 = tf.transpose(a=patch1, perm=[0, 1, 2, 4, 3])
        patch2 = tf.compat.v1.extract_image_patches(fg_in, [1, k_size, k_size, 1], [1, 1, 1, 1], [1, 1, 1, 1], 'SAME')

        ACL = []
        fuse_weight = tf.reshape(tf.eye(3), [3, 3, 1, 1])

        for ib in range(b):
            k1 = patch1[ib, :, :, :, :]
            k2 = k1 / tf.sqrt(tf.reduce_sum(input_tensor=tf.square(k1), axis=2, keepdims=True) + 1e-16)
            k1 = tf.reshape(k1, (k_size, k_size, dims, c))
            ww = patch2[ib, :, :, :]
            ft = ww / tf.sqrt(tf.reduce_sum(input_tensor=tf.square(ww), axis=2, keepdims=True) + 1e-16)
            ft = tf.expand_dims(ft, 0)
            CA = tf.nn.conv2d(input=ft, filters=k2, strides=[1, 1, 1, 1], padding='SAME')
            CA = tf.reshape(CA, [1, h * w, c, 1])
            CA = tf.nn.conv2d(input=CA, filters=fuse_weight, strides=[1, 1, 1, 1], padding='SAME')
            CA = tf.reshape(CA, [1, h, w, int(math.sqrt(c)), int(math.sqrt(c))])
            CA = tf.transpose(a=CA, perm=[0, 2, 1, 4, 3])
            CA = tf.reshape(CA, [1, h * w, c, 1])
            CA = tf.nn.conv2d(input=CA, filters=fuse_weight, strides=[1, 1, 1, 1], padding='SAME')
            CA = tf.reshape(CA, [1, h, w, int(math.sqrt(c)), int(math.sqrt(c))])
            CA = tf.transpose(a=CA, perm=[0, 2, 1, 4, 3])
            CA = tf.reshape(CA, [1, h, w, c])
            CA2 = softmax(lamda * CA)
            ACLt = tf.nn.conv2d_transpose(CA2, k1, output_shape=[1, h, w, dims], strides=[1, 1, 1, 1], padding='SAME')
            ACLt = ACLt / (k_size ** 2)

            if ib == 0:
                ACL = ACLt
            else:
                ACL = tf.concat((ACL, ACLt), 0)

        ACL2 = bg + ACL * (1.0 - mask_r)
        return ACL2
