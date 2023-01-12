#include <iostream>
#include <stdlib.h>
#include <fstream>

struct medicion{

    int intensidad;
    int destino;
    int observacion;
    int input;
    int index;
};

int main(){
  
    struct medicion datos;
    FILE *archivo = fopen("datos.bin","rb");
    fread(&datos, sizeof(struct medicion),1, archivo);  
    fclose(archivo);

    printf("la intensidad es = %d \n", datos.intensidad);
    printf("el destino es = %d\n", datos.destino);
    printf("el obstaculo esta en = %d\n", datos.observacion);
    printf("el input es = %d\n", datos.input);
    printf("el indice es = %d\n", datos.index);

    system("pause");
    return 0;

}