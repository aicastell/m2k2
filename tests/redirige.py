import sys,string

class RedirigeError:
  def __init__(self, desde=sys.stdout):
    self.desde= desde
    self.estrella= 1

  def write(self, l):
    if self.estrella:
       self.desde.write("* ")
       self.estrella= 0
    for i in l:
       if self.estrella:
          self.desde.write("* ")
       self.desde.write(i)
       self.estrella= i=="\n"
    
  def flush(self):
    pass

class RedirigeEntrada:
  def __init__(self, entrada):
    self.entrada= entrada
    self.nlinea= 1
    self.buffer= ""

  def emite(self,l):
    sys.stdout.write("=======================================\n")
    sys.stdout.write("Línea: %d\n" % self.nlinea)
    a= string.split(l,"@ ")
    if len(a)==1:
      sys.stdout.write("Declaración: "+l+"\n")
    else:
      sys.stdout.write("Entrada: %s\nEsperado: %s" %(a[0],a[1]))
    self.nlinea= self.nlinea+1

  def read(self, n):
    if n!= 1:
	sys.stdout("ERROR EN REDIRIGE: Leído más de un carácter")
    if self.buffer=="":
       l= self.entrada.readline()
       if not l:
         return ""
       self.emite(l)
       pos= string.find(l,"@")
       if pos!=-1:
          if l[-1]=="\n":
            self.buffer= l[:pos]+"\n"
          else:
            return l[:pos]
       else:
         self.buffer= l

    c= self.buffer[0]
    self.buffer= self.buffer[1:]
    return c

  def readline(self):
    l= self.entrada.readline()
    if l:
      self.emite(l)
    pos= string.find(l,"@")
    if pos==-1:
      return l
    elif l[-1]=="\n":
      return l[:pos]+"\n"
    else:
      return l[:pos]

  def isatty(self):
    return 0

  def close(self):
    pass

  def flush(self):
    pass
