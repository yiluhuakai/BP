  1 #coding:utf-8
  2 import random
  3 import math
  4 
  5 #
  6 #   �������ͣ�
  7 #   "pd_" ��ƫ����ǰ׺
  8 #   "d_" ��������ǰ׺
  9 #   "w_ho" �������㵽������Ȩ��ϵ������
 10 #   "w_ih" ������㵽�������Ȩ��ϵ��������
 11 
 12 class NeuralNetwork:
 13     LEARNING_RATE = 0.5
 14 
 15     def __init__(self, num_inputs, num_hidden, num_outputs, hidden_layer_weights = None, hidden_layer_bias = None, output_layer_weights = None, output_layer_bias = None):
 16         self.num_inputs = num_inputs
 17 
 18         self.hidden_layer = NeuronLayer(num_hidden, hidden_layer_bias)
 19         self.output_layer = NeuronLayer(num_outputs, output_layer_bias)
 20 
 21         self.init_weights_from_inputs_to_hidden_layer_neurons(hidden_layer_weights)
 22         self.init_weights_from_hidden_layer_neurons_to_output_layer_neurons(output_layer_weights)
 23 
 24     def init_weights_from_inputs_to_hidden_layer_neurons(self, hidden_layer_weights):
 25         weight_num = 0
 26         for h in range(len(self.hidden_layer.neurons)):
 27             for i in range(self.num_inputs):
 28                 if not hidden_layer_weights:
 29                     self.hidden_layer.neurons[h].weights.append(random.random())
 30                 else:
 31                     self.hidden_layer.neurons[h].weights.append(hidden_layer_weights[weight_num])
 32                 weight_num += 1
 33 
 34     def init_weights_from_hidden_layer_neurons_to_output_layer_neurons(self, output_layer_weights):
 35         weight_num = 0
 36         for o in range(len(self.output_layer.neurons)):
 37             for h in range(len(self.hidden_layer.neurons)):
 38                 if not output_layer_weights:
 39                     self.output_layer.neurons[o].weights.append(random.random())
 40                 else:
 41                     self.output_layer.neurons[o].weights.append(output_layer_weights[weight_num])
 42                 weight_num += 1
 43 
 44     def inspect(self):
 45         print('------')
 46         print('* Inputs: {}'.format(self.num_inputs))
 47         print('------')
 48         print('Hidden Layer')
 49         self.hidden_layer.inspect()
 50         print('------')
 51         print('* Output Layer')
 52         self.output_layer.inspect()
 53         print('------')
 54 
 55     def feed_forward(self, inputs):
 56         hidden_layer_outputs = self.hidden_layer.feed_forward(inputs)
 57         return self.output_layer.feed_forward(hidden_layer_outputs)
 58 
 59     def train(self, training_inputs, training_outputs):
 60         self.feed_forward(training_inputs)
 61 
 62         # 1. �����Ԫ��ֵ
 63         pd_errors_wrt_output_neuron_total_net_input = [0] * len(self.output_layer.neurons)
 64         for o in range(len(self.output_layer.neurons)):
 65 
 66             # ?E/?z?
 67             pd_errors_wrt_output_neuron_total_net_input[o] = self.output_layer.neurons[o].calculate_pd_error_wrt_total_net_input(training_outputs[o])
 68 
 69         # 2. ��������Ԫ��ֵ
 70         pd_errors_wrt_hidden_neuron_total_net_input = [0] * len(self.hidden_layer.neurons)
 71         for h in range(len(self.hidden_layer.neurons)):
 72 
 73             # dE/dy? = �� ?E/?z? * ?z/?y? = �� ?E/?z? * w??
 74             d_error_wrt_hidden_neuron_output = 0
 75             for o in range(len(self.output_layer.neurons)):
 76                 d_error_wrt_hidden_neuron_output += pd_errors_wrt_output_neuron_total_net_input[o] * self.output_layer.neurons[o].weights[h]
 77 
 78             # ?E/?z? = dE/dy? * ?z?/?
 79             pd_errors_wrt_hidden_neuron_total_net_input[h] = d_error_wrt_hidden_neuron_output * self.hidden_layer.neurons[h].calculate_pd_total_net_input_wrt_input()
 80 
 81         # 3. ���������Ȩ��ϵ��
 82         for o in range(len(self.output_layer.neurons)):
 83             for w_ho in range(len(self.output_layer.neurons[o].weights)):
 84 
 85                 # ?E?/?w?? = ?E/?z? * ?z?/?w??
 86                 pd_error_wrt_weight = pd_errors_wrt_output_neuron_total_net_input[o] * self.output_layer.neurons[o].calculate_pd_total_net_input_wrt_weight(w_ho)
 87 
 88                 # ��w = �� * ?E?/?w?
 89                 self.output_layer.neurons[o].weights[w_ho] -= self.LEARNING_RATE * pd_error_wrt_weight
 90 
 91         # 4. �����������Ȩ��ϵ��
 92         for h in range(len(self.hidden_layer.neurons)):
 93             for w_ih in range(len(self.hidden_layer.neurons[h].weights)):
 94 
 95                 # ?E?/?w? = ?E/?z? * ?z?/?w?
 96                 pd_error_wrt_weight = pd_errors_wrt_hidden_neuron_total_net_input[h] * self.hidden_layer.neurons[h].calculate_pd_total_net_input_wrt_weight(w_ih)
 97 
 98                 # ��w = �� * ?E?/?w?
 99                 self.hidden_layer.neurons[h].weights[w_ih] -= self.LEARNING_RATE * pd_error_wrt_weight
100 
101     def calculate_total_error(self, training_sets):
102         total_error = 0
103         for t in range(len(training_sets)):
104             training_inputs, training_outputs = training_sets[t]
105             self.feed_forward(training_inputs)
106             for o in range(len(training_outputs)):
107                 total_error += self.output_layer.neurons[o].calculate_error(training_outputs[o])
108         return total_error
109 
110 class NeuronLayer:
111     def __init__(self, num_neurons, bias):
112 
113         # ͬһ�����Ԫ����һ���ؾ���b
114         self.bias = bias if bias else random.random()
115 
116         self.neurons = []
117         for i in range(num_neurons):
118             self.neurons.append(Neuron(self.bias))
119 
120     def inspect(self):
121         print('Neurons:', len(self.neurons))
122         for n in range(len(self.neurons)):
123             print(' Neuron', n)
124             for w in range(len(self.neurons[n].weights)):
125                 print('  Weight:', self.neurons[n].weights[w])
126             print('  Bias:', self.bias)
127 
128     def feed_forward(self, inputs):
129         outputs = []
130         for neuron in self.neurons:
131             outputs.append(neuron.calculate_output(inputs))
132         return outputs
133 
134     def get_outputs(self):
135         outputs = []
136         for neuron in self.neurons:
137             outputs.append(neuron.output)
138         return outputs
139 
140 class Neuron:
141     def __init__(self, bias):
142         self.bias = bias
143         self.weights = []
144 
145     def calculate_output(self, inputs):
146         self.inputs = inputs
147         self.output = self.squash(self.calculate_total_net_input())
148         return self.output
149 
150     def calculate_total_net_input(self):
151         total = 0
152         for i in range(len(self.inputs)):
153             total += self.inputs[i] * self.weights[i]
154         return total + self.bias
155 
156     # �����sigmoid
157     def squash(self, total_net_input):
158         return 1 / (1 + math.exp(-total_net_input))
159 
160 
161     def calculate_pd_error_wrt_total_net_input(self, target_output):
162         return self.calculate_pd_error_wrt_output(target_output) * self.calculate_pd_total_net_input_wrt_input();
163 
164     # ÿһ����Ԫ���������ƽ���ʽ�����
165     def calculate_error(self, target_output):
166         return 0.5 * (target_output - self.output) ** 2
167 
168     
169     def calculate_pd_error_wrt_output(self, target_output):
170         return -(target_output - self.output)
171 
172     
173     def calculate_pd_total_net_input_wrt_input(self):
174         return self.output * (1 - self.output)
175 
176 
177     def calculate_pd_total_net_input_wrt_weight(self, index):
178         return self.inputs[index]
179 
180 
181 # ���е�����:
182 
183 nn = NeuralNetwork(2, 2, 2, hidden_layer_weights=[0.15, 0.2, 0.25, 0.3], hidden_layer_bias=0.35, output_layer_weights=[0.4, 0.45, 0.5, 0.55], output_layer_bias=0.6)
184 for i in range(10000):
185     nn.train([0.05, 0.1], [0.01, 0.09])
186     print(i, round(nn.calculate_total_error([[[0.05, 0.1], [0.01, 0.09]]]), 9))
187 
188 
189 #����һ�����ӣ����԰����������ע�͵�������һ��:
190 
191 # training_sets = [
192 #     [[0, 0], [0]],
193 #     [[0, 1], [1]],
194 #     [[1, 0], [1]],
195 #     [[1, 1], [0]]
196 # ]
197 
198 # nn = NeuralNetwork(len(training_sets[0][0]), 5, len(training_sets[0][1]))
199 # for i in range(10000):
200 #     training_inputs, training_outputs = random.choice(training_sets)
201 #     nn.train(training_inputs, training_outputs)
202 #     print(i, nn.calculate_total_error(training_sets))