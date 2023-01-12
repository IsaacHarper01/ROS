#include<stdlib.h>
#include<iostream>

class Rectangulo{
      private:
        float ancho, largo;
      public:
        Rectangulo(float,float);
        void area();
        void perimetro();
};

Rectangulo::Rectangulo(float _largo, float _ancho){
    ancho = _ancho;
    largo = _largo;
}

void Rectangulo::perimetro(){
    float _perimetro;
    _perimetro = largo*2 + ancho*2;
     printf("el perimetro es: %0.2f metros \n",_perimetro); 
}

void Rectangulo::area(){
    float _area;
    _area = largo*ancho;
    printf("el area es %0.2f metros cuadrados \n", _area);
}

int main(){


Rectangulo r1(10, 12.5);

r1.area();
r1.perimetro();
system("pause");
return 0;

}