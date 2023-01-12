
#define NUM_BITS_INPUTS 4
#define NUM_MAX_INPUTS 256// 2 >> NUM_BITS_INPUTS+NUM_BITS_STATES
#define NUM_BITS_OUTPUTS 4 // bits to decode 8 outputs: STOP, BACKWARD, FORWARD, TURN_LEFT, TURN_RIGHT, etc
#define NUM_MAX_OUTPUTS 16
#define NUM_BITS_INTENSITY 2 //necesary bits to represent the light intensity
#define NUM_BITS_DEST_ANGLE 3 //necesary bits to represent the light direcction
#define NUM_MAX_MEMORY 65535 // 2 >> 16
#define NUM_MAX_MEMORY_INPUT 1024 // 2 >> 10
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <time.h>
#include <sys/time.h>
#include <unistd.h>

typedef struct _memory_state_machine{
        int state;
        int output;
} memory_state_machine;

int  read_state_machine(char *file,int *memory_state,int *num_bits_out,int *num_in,int *memory_output){

 int i,j;
 FILE *fpr;
 int flag=1;
 int x,num_bits_state,num_bits_output,num_inputs;
 int state=0,output=0;


 printf("File %s\n",file);



 if((fpr=fopen(file,"r")) == NULL){
        printf("File %s can not be open\n",file);
        exit(0);
 }

 fscanf(fpr,"%d",&num_bits_state);
 fscanf(fpr,"%d",&num_bits_output);
 fscanf(fpr,"%d",&num_inputs);

 printf(" Num. bits state %d num. bits output %d num_inputs %d \n",
                                num_bits_state,num_bits_output,num_inputs);


 j=1;
 while(flag){
        for(i=1;i<=num_bits_state;i++){

                if(fscanf(fpr,"%d",&x) == EOF)
                        flag=0;
                else{
                        state = (x << (num_bits_state-i)) + state;
                }
        }

        for(i=1;i<=num_bits_output;i++){

                if(fscanf(fpr,"%d",&x) == EOF)
                        flag=0;
                else{
                        output= (x << (num_bits_output-i)) + output;
                }
        }


	memory_state[j]=state;
       	memory_output[j]=output;

       	printf("memory[%d] state %d output %d\n",j,memory_state[j],memory_output[j]);


        state=0;
        output=0;


        j++;

        if(j==NUM_MAX_MEMORY){
                printf(" Increase constant NUM_MAX_MEMORY in file ~/robotics/state_machines/state_machine_engine.h\n");
                exit(0);
        }
 }

 j--;

 printf("Num. memory locations %d\n",j-1);
 printf("Num. total memory %d\n",2<<(num_bits_state+num_inputs-1));

 for(i=j;i< (2<<(num_bits_state+num_inputs-1)); i++){

        memory_state[i]=0;
        memory_output[i]=0;

        printf("memory[%d] state %d output %d\n",i,memory_state[i],memory_output[i]);


 }


 fclose(fpr);

 *num_in=num_inputs;
 *num_bits_out=num_bits_output;

 return(2<<(num_bits_state+num_inputs-1));

}
void state_machine_engine(int obs, int dest, int detection_bit, int state, int *next_state,float Mag_Advance,float max_angle,
					 int num_bits_vq)
{
        static int *mem_state,*mem_output;
        static int flg_read=1;
        static int num_bits_input = NUM_BITS_INPUTS, num_bits_output=NUM_BITS_OUTPUTS;
        int size_mem;
        int index;
        int out;
        int input;
        int num_bits_intensity = 2;
        int num_bits_dest_angle = 3;
        char state_machine_file_name[300] = "memoria_robotAP.txt";
        if(flg_read==1){
        mem_state= (int *) malloc((unsigned) NUM_MAX_MEMORY*sizeof(int));
        mem_output= (int *) malloc((unsigned) NUM_MAX_MEMORY*sizeof(int));

        size_mem=read_state_machine(state_machine_file_name,mem_state,&num_bits_output,&num_bits_input,mem_output);
        flg_read=0;
                        }
        
        printf("detection_bit %d obstacle %d destinaiton %d\n",detection_bit,obs,dest);
        
        //input = (intensity << 4) + (obs << 2) + dest;
        if (detection_bit==1){
        input =  (detection_bit << num_bits_dest_angle) + obs;
                             }
        else {
        input = (detection_bit << num_bits_dest_angle) + dest;
             }

        index = (((state) << num_bits_input) + input+1) & 0xffff;


        printf("present state %d input %d\n",state,input);
        printf("num_bits_dest_angle = %d, num_bits_vq = %d\n ",num_bits_dest_angle, num_bits_vq);
        

        *next_state = mem_state[index];
        out = mem_output[index];
        
        printf("index %d next_state %d out %d\n",index,*next_state,out);
        

        // /home/biorobotica/robotics/utilities/utilities.h //
        //gen_vector=generate_output(out,Mag_Advance,max_angle);
        //printf("Next State: %d\n", *next_state);
        //return gen_vector;
}


int main(){
        int next_s = 2;
        //obs, dest, detection_bit,state,next_state,mag_advance,max_angle,bits_vq
        state_machine_engine(6,3,0,3, &next_s,0.1,0.74,2);
        
}