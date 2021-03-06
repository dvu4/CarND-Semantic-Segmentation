import os.path
import tensorflow as tf
import helper
import warnings
from distutils.version import LooseVersion
import project_tests as tests


# Check TensorFlow Version
assert LooseVersion(tf.__version__) >= LooseVersion('1.0'), 'Please use TensorFlow version 1.0 or newer.  You are using {}'.format(tf.__version__)
print('TensorFlow Version: {}'.format(tf.__version__))

# Check for a GPU
if not tf.test.gpu_device_name():
    warnings.warn('No GPU found. Please use a GPU to train your neural network.')
else:
    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))


def load_vgg(sess, vgg_path):
    """
    Load Pretrained VGG Model into TensorFlow.
    :param sess: TensorFlow Session
    :param vgg_path: Path to vgg folder, containing "variables/" and "saved_model.pb"
    :return: Tuple of Tensors from VGG model (image_input, keep_prob, layer3_out, layer4_out, layer7_out)
    """
    # TODO: Implement function
    #   Use tf.saved_model.loader.load to load the model and weights
    vgg_tag = 'vgg16'
    vgg_input_tensor_name = 'image_input:0'
    vgg_keep_prob_tensor_name = 'keep_prob:0'
    vgg_layer3_out_tensor_name = 'layer3_out:0'
    vgg_layer4_out_tensor_name = 'layer4_out:0'
    vgg_layer7_out_tensor_name = 'layer7_out:0'
    
    #tf.saved_model.loader.load(sess,tags,export_dir,**saver_kwargs)
    #model = tf.saved_model.loader.load(session, ['serve'], "simple-cross/export/1494601566/")
    tf.saved_model.loader.load(sess, [vgg_tag], vgg_path)
    
    #vgg_input     = get_default_graph().get_tensor_by_name(vgg_input_tensor_name)
    vgg_input      = sess.graph.get_tensor_by_name(vgg_input_tensor_name)
    vgg_keep_prob  = sess.graph.get_tensor_by_name(vgg_keep_prob_tensor_name)
    vgg_layer3_out = sess.graph.get_tensor_by_name(vgg_layer3_out_tensor_name)
    vgg_layer4_out = sess.graph.get_tensor_by_name(vgg_layer4_out_tensor_name)
    vgg_layer7_out = sess.graph.get_tensor_by_name(vgg_layer7_out_tensor_name)

    return vgg_input, vgg_keep_prob, vgg_layer3_out, vgg_layer4_out, vgg_layer7_out 

tests.test_load_vgg(load_vgg, tf)


def layers(vgg_layer3_out, vgg_layer4_out, vgg_layer7_out, num_classes):
    """
    Create the layers for a fully convolutional network.  Build skip-layers using the vgg layers.
    :param vgg_layer7_out: TF Tensor for VGG Layer 3 output
    :param vgg_layer4_out: TF Tensor for VGG Layer 4 output
    :param vgg_layer3_out: TF Tensor for VGG Layer 7 output
    :param num_classes: Number of classes to classify
    :return: The Tensor for the last layer of output
    """
    # TODO: Implement function

    #conv2d(inputs,filters,kernel_size,strides=(1, 1),padding='valid', kernel_initializer=None, kernel_regularizer=None)
    
    # The third argument, 1, is the kernel size, meaning this is a 1 by 1 convolution. 
    # Thus far, we’ve downsampled the input image and extracted features using the VGG16 encoder. 
    # We’ve also replaced the linear layers with 1 by 1 convolutional layers, preserving spatial information.
    
    # 1 by 1 convolution of vgg_layer7
    layer7_output = tf.layers.conv2d(vgg_layer7_out, 
                                     num_classes, 
                                     1, 
                                     strides=(1,1), 
                                     padding='same',
                                     kernel_initializer= tf.random_normal_initializer(stddev=0.01),
                                     kernel_regularizer= tf.contrib.layers.l2_regularizer(1e-3))
    
    # upsample the input to the original image size. The shape of the tensor after the final convolutional transpose layer will be 4-dimensional: (batch_size, original_height, original_width, num_classes). 
    #The transpose convolutional layers increase the height and width dimensions of the 4D input Tensor.
    
    #decoder -  upsampling
    layer4_input1  = tf.layers.conv2d_transpose(layer7_output, 
                                                num_classes, 
                                                4, 
                                                strides=(2, 2),
                                                padding='same',
                                                kernel_initializer= tf.random_normal_initializer(stddev=0.01),
                                                kernel_regularizer= tf.contrib.layers.l2_regularizer(1e-3))
    # 1 by 1 convolution of vgg_layer4
    layer4_input2 = tf.layers.conv2d(vgg_layer4_out, 
                                     num_classes, 
                                     1, 
                                     strides=(1,1), 
                                     padding='same',
                                     kernel_initializer= tf.random_normal_initializer(stddev=0.01),
                                     kernel_regularizer= tf.contrib.layers.l2_regularizer(1e-3))
    
    # The final step is adding skip connections to the model. In order to do this we’ll combine the output of two layers. The first output is the output of the current layer. The second output is the output of a layer further back in the network, typically a pooling layer. In the following example we combine the result of the previous layer with the result of the 4th pooling layer through elementwise addition (tf.add).
    
    #skip connection
    layer4_output = tf.add(layer4_input1, layer4_input2)
    
    #decoder -  upsampling
    layer3_input1  = tf.layers.conv2d_transpose(layer4_output, 
                                                num_classes, 
                                                4, 
                                                strides=(2, 2),
                                                padding='same',
                                                kernel_initializer= tf.random_normal_initializer(stddev=0.01),
                                                kernel_regularizer= tf.contrib.layers.l2_regularizer(1e-3))
    
    # 1 by 1 convolution of vgg_layer3
    layer3_input2 = tf.layers.conv2d(vgg_layer3_out, 
                                     num_classes, 
                                     1, 
                                     strides=(1,1), 
                                     padding='same',
                                     kernel_initializer= tf.random_normal_initializer(stddev=0.01),
                                     kernel_regularizer= tf.contrib.layers.l2_regularizer(1e-3))
    
    #skip connection
    layer3_output = tf.add(layer3_input1, layer3_input2)
    
    
    #decoder -  upsampling according to paper for FCN8 (fig. 3)
    nn_last_layer  = tf.layers.conv2d_transpose(layer3_output, 
                                                num_classes, 
                                                16, 
                                                strides=(8, 8),
                                                padding='same',
                                                kernel_initializer= tf.random_normal_initializer(stddev=0.01),
                                                kernel_regularizer= tf.contrib.layers.l2_regularizer(1e-3))
    
    
    return nn_last_layer

tests.test_layers(layers)


def optimize(nn_last_layer, correct_label, learning_rate, num_classes):
    """
    Build the TensorFLow loss and optimizer operations.
    :param nn_last_layer: TF Tensor of the last layer in the neural network
    :param correct_label: TF Placeholder for the correct label image
    :param learning_rate: TF Placeholder for the learning rate
    :param num_classes: Number of classes to classify
    :return: Tuple of (logits, train_op, cross_entropy_loss)
    """
    # TODO: Implement function
    
    #The final step is to define a loss. That way, we can approach training a FCN just like we would approach training a normal classification CNN.

    #In the case of a FCN, the goal is to assign each pixel to the appropriate class. We already happen to know a great loss function for this setup, cross entropy loss! Remember the output tensor is 4D so we have to reshape it to 2D:

    #logits is now a 2D tensor where each row represents a pixel and each column a class. 
    logits = tf.reshape(nn_last_layer, (-1, num_classes))
    
    labels = tf.reshape(correct_label, (-1, num_classes))
    
    
    
    #loss function
    cross_entropy_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits= logits, labels= labels))
                         
    
    #train operation 
    train_op = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy_loss)
    
    return logits, train_op, cross_entropy_loss

tests.test_optimize(optimize)


def train_nn(sess, epochs, batch_size, get_batches_fn, train_op, cross_entropy_loss, input_image,
             correct_label, keep_prob, learning_rate):
    """
    Train neural network and print out the loss during training.
    :param sess: TF Session
    :param epochs: Number of epochs
    :param batch_size: Batch size
    :param get_batches_fn: Function to get batches of training data.  Call using get_batches_fn(batch_size)
    :param train_op: TF Operation to train the neural network
    :param cross_entropy_loss: TF Tensor for the amount of loss
    :param input_image: TF Placeholder for input images
    :param correct_label: TF Placeholder for label images
    :param keep_prob: TF Placeholder for dropout keep probability
    :param learning_rate: TF Placeholder for learning rate
    """
    # TODO: Implement function
    for epoch_i in range(epochs):
        for images, labels in get_batches_fn(batch_size):
            _, loss = sess.run([train_op, cross_entropy_loss],feed_dict={input_image : images, 
                                                                         correct_label : labels,
                                                                         keep_prob : 0.5, 
                                                                         learning_rate : 0.0001})
            print('Epoch {}/{}; Training Loss:{:.03f}'.format(epoch_i+1, epochs, loss))
    
    #pass
tests.test_train_nn(train_nn)


def run():
    num_classes = 2
    image_shape = (160, 576)
    data_dir = './data'
    runs_dir = './runs'
    tests.test_for_kitti_dataset(data_dir)

    # Download pretrained vgg model
    helper.maybe_download_pretrained_vgg(data_dir)

    # OPTIONAL: Train and Inference on the cityscapes dataset instead of the Kitti dataset.
    # You'll need a GPU with at least 10 teraFLOPS to train on.
    #  https://www.cityscapes-dataset.com/

    epochs = 50
    batch_size = 5
    with tf.Session() as sess:
        # Path to vgg model
        vgg_path = os.path.join(data_dir, 'vgg')
        # Create function to get batches
        get_batches_fn = helper.gen_batch_function(os.path.join(data_dir, 'data_road/training'), image_shape)

        # OPTIONAL: Augment Images for better results
        #  https://datascience.stackexchange.com/questions/5224/how-to-prepare-augment-images-for-neural-network

        # TODO: Build NN using load_vgg, layers, and optimize function
        
        # TF Placeholders
        correct_label = tf.placeholder(dtype=tf.float32, shape=(None, None, None, num_classes), name='correct_label')
        learning_rate = tf.placeholder(dtype=tf.float32, name='learning_rate')
        
        
        vgg_input, vgg_keep_prob, vgg_layer3_out, vgg_layer4_out, vgg_layer7_out = load_vgg(sess, vgg_path)
        
        nn_last_layer = layers(vgg_layer3_out, vgg_layer4_out, vgg_layer7_out, num_classes)

        logits, train_op, cross_entropy_loss = optimize(nn_last_layer, correct_label, learning_rate, num_classes)
        
      
        # TODO: Train NN using the train_nn function
        sess.run(tf.global_variables_initializer())
        train_nn(sess, 
                 epochs, 
                 batch_size, 
                 get_batches_fn, 
                 train_op, 
                 cross_entropy_loss, 
                 vgg_input, 
                 correct_label, 
                 vgg_keep_prob, 
                 learning_rate)
        
        
        # 'Saver' op to save and restore all the variables
        saver = tf.train.Saver()
        save_path = saver.save(sess, 'checkpoints/model1.ckpt')
        saver.export_meta_graph('checkpoints/model1.meta')
        tf.train.write_graph(sess.graph_def, './checkpoints/', 'model1.pb', False)
        print("Model saved in file: %s" % save_path)
        
        
        # TODO: Save inference data using helper.save_inference_samples
        #  helper.save_inference_samples(runs_dir, data_dir, sess, image_shape, logits, keep_prob, input_image)
        helper.save_inference_samples(runs_dir, data_dir, sess, image_shape, logits, vgg_keep_prob, vgg_input )
        # OPTIONAL: Apply the trained model to a video


                 
if __name__ == '__main__':
    run()