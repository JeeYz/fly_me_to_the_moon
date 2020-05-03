import tensorflow as tf

x = [[2.]]
m = tf.matmul(x, x)
print("hello, {}".format(m))

a = tf.constant([[1, 2],
				[3, 4]])
print(a)

b = tf.add(a, 1)
print(b)

print(a * b)

import numpy as np

c = np.multiply(a, b)
print(c)

print(a.numpy())

def fizzbuzz(max_num):
	counter = tf.constant(0)
	max_num = tf.convert_to_tensor(max_num)
	for num in range(1, max_num.numpy()+1):
		num = tf.constant(num)
		if int(num % 3) == 0 and int(num % 5) == 0:
			print("FizzBuzz")
		elif int(num % 3) == 0:
			print("Fizz")
		elif int(num % 5) == 0:
			print("Buzz")
		else:
			print(num.numpy())
		counter += 1

fizzbuzz(15)

w = tf.Variable([[1.0]])
with tf.GradientTape() as tape:
	loss = w * w

grad = tape.gradient(loss, w)
print(grad)

"""
(mnist_images, mnist_labels), _ = tf.keras.datasets.mnist.load_data()

dataset = tf.data.Dataset.from_tensor_slices(
	(tf.cast(mnist_images[...,tf.newaxis]/255, tf.float32),
	tf.cast(mnist_labels, tf.int64)))
dataset = dataset.shuffle(1000).batch(32)

mnist_model = tf.keras.Sequential([
	tf.keras.layers.Conv2D(16,[3,3], activation='relu',
													input_shape=(None, None, 1)),
	tf.keras.layers.Conv2D(16,[3,3], activation='relu'),
	tf.keras.layers.GlobalAveragePooling2D(),
	tf.keras.layers.Dense(10)
])

for images, labels in dataset.take(1):
	print("로짓: ", mnist_model(images[0:1]).numpy())

optimizer = tf.keras.optimizers.Adam()
loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

loss_history = []

def train_step(images, labels):
	with tf.GradientTape() as tape:
		logits = mnist_model(images, training=True)

		tf.debugging.assert_equal(logits.shape, (32, 10))
		
		loss_value = loss_object(labels, logits)

	loss_history.append(loss_value.numpy().mean())
	grads = tape.gradient(loss_value, mnist_model.trainable_variables)
	optimizer.apply_gradients(zip(grads, mnist_model.trainable_variables))

def train():
	for epoch in range(1):
		for (batch, (images, labels)) in enumerate(dataset):
			train_step(images, labels)
		print('에포크 {} 종료'.format(epoch))

train()


import matplotlib.pyplot as plt

plt.plot(loss_history)
plt.xlabel('Batch #')
plt.ylabel('Loss [entropy]')
"""

class Model(tf.keras.Model):
  def __init__(self):
    super(Model, self).__init__()
    self.W = tf.Variable(5., name='weight')
    self.B = tf.Variable(10., name='bias')
  def call(self, inputs):
    return inputs * self.W + self.B

# 약 3 * x + 2개의 점으로 구성된 실험 데이터
NUM_EXAMPLES = 2000
training_inputs = tf.random.normal([NUM_EXAMPLES])
noise = tf.random.normal([NUM_EXAMPLES])
training_outputs = training_inputs * 3 + 2 + noise

# 최적화할 손실함수
def loss(model, inputs, targets):
  error = model(inputs) - targets
  return tf.reduce_mean(tf.square(error))

def grad(model, inputs, targets):
  with tf.GradientTape() as tape:
    loss_value = loss(model, inputs, targets)
  return tape.gradient(loss_value, [model.W, model.B])

# 정의:
# 1. 모델
# 2. 모델 파라미터에 대한 손실 함수의 미분
# 3. 미분에 기초한 변수 업데이트 전략
model = Model()
optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)

print("초기 손실: {:.3f}".format(loss(model, training_inputs, training_outputs)))

# 반복 훈련
for i in range(300):
  grads = grad(model, training_inputs, training_outputs)
  optimizer.apply_gradients(zip(grads, [model.W, model.B]))
  if i % 20 == 0:
    print("스텝 {:03d}에서 손실: {:.3f}".format(i, loss(model, training_inputs, training_outputs)))

print("최종 손실: {:.3f}".format(loss(model, training_inputs, training_outputs)))
print("W = {}, B = {}".format(model.W.numpy(), model.B.numpy()))








