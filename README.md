# reconhecimentoBotoesEDigitosElevadorComInputVoz


Primeiramente é necessário rodar o jack-server:
$ jack_control start


Para teste apenas do input de voz:
$ python3 getVoice.py


1. Para iniciar os teste em vídeo em tempo real, deve-se rodar o programa malha.py o qual irá:

- Chamar o algortimo getVoice.py, para:
  - Executar text-to-speech para perguntar a pessoa qual andar ela pretende ir
  - Executar speech-to-text ao receber uma entrada de voz
  - Reconhecer as palavras ditas e coloca-las em uma lista
  - Percorrer a lista procurando por números de andares, caso contrário pedir novamente que seja dito o andar onde a pessoa deseja seguir
 
- Capturar o vídeo da câmera webcam (também é possível capturar vídeo da câmera do celular através do aplicativo para android IP webcam, que irá fornecer uma url de stream do vídeo) 

- Aplicar os filtros e cortes necessários. OBS: para maior eficiência no reconhecimento de dígitos não é recomendado o uso de Laplacian nos frames.

- Chamar a função 'prediction', que irá:
  - Preparar o frame em escala de cinza para ser analisado
  - Redimensiona-lo e aplicar o modelo de predição da biblioteca KERAS de deep learning, retornando a probabilidade e o resultado encontrado no frame em questão analisado
 
- Caso a probabilidade seja superior ou igual a 0.999 e o resultado seja o número do andar dito pela pessoa no speech-to-text, o programa é encerrado retornando as coordenadas do botão próximo ao dígito localizado no vídeo em tempo real.
