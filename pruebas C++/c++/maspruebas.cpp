/********************************************************
 *                                                      *
 *                                                      *
 *      state_machine_robotAP.h		          	*
 *                                                      *
 *		Jesus Savage				*
 *		FI-UNAM					*
 *		12-2-2022                               *
 *                                                      *
 ********************************************************/

#define NUM_BITS_INPUTS 4
#define NUM_MAX_INPUTS 256// 2 >> NUM_BITS_INPUTS+NUM_BITS_STATES
#define NUM_BITS_OUTPUTS 4 // bits to decode 8 outputs: STOP, BACKWARD, FORWARD, TURN_LEFT, TURN_RIGHT, etc
#define NUM_MAX_OUTPUTS 16
#define NUM_BITS_DETECTION 2 //necesary bits to represent the light intensity
#define NUM_BITS_DEST_ANGLE 3 //necesary bits to represent the light direcction
#define NUM_MAX_MEMORY 65535 // 2 >> 16
#define NUM_MAX_MEMORY_INPUT 1024 // 2 >> 10



int  read_state_machine_robotAP(char *file,int *memory_state,int *num_bits_out,int *num_in,int *memory_output){

 int i,j;
 FILE *fpr;
 int flag=1;
 int x,num_bits_state,num_bits_output,num_inputs;
 int state=0,output=0;

#ifdef DEBUG
 printf("File %s\n",file);
#endif


 if((fpr=fopen(file,"r")) == NULL){
        printf("File %s can not be open\n",file);
        exit(0);
 }

 fscanf(fpr,"%d",&num_bits_state);
 fscanf(fpr,"%d",&num_bits_output);
 fscanf(fpr,"%d",&num_inputs);
#ifdef DEBUG
 printf(" Num. bits state %d num. bits output %d num_inputs %d \n",
                                num_bits_state,num_bits_output,num_inputs);
#endif

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
#ifdef DEBUG
       	printf("memory[%d] state %d output %d\n",j,memory_state[j],memory_output[j]);
#endif

        state=0;
        output=0;


        j++;

        if(j==NUM_MAX_MEMORY){
                printf(" Increase constant NUM_MAX_MEMORY in file ~/robotics/state_machines/state_machine_engine.h\n");
                exit(0);
        }


 }

 j--;
#ifdef DEBUG
 printf("Num. memory locations %d\n",j-1);
 printf("Num. total memory %d\n",2<<(num_bits_state+num_inputs-1));
#endif

 for(i=j;i< (2<<(num_bits_state+num_inputs-1)); i++){

        memory_state[i]=0;
        memory_output[i]=0;
#ifdef DEBUG
        printf("memory[%d] state %d output %d\n",i,memory_state[i],memory_output[i]);
#endif

 }


 fclose(fpr);

 *num_in=num_inputs;
 *num_bits_out=num_bits_output;

 return(2<<(num_bits_state+num_inputs-1));

}


// State Machine engine 
AdvanceAngle state_machine_robotAP(int obs, int dest, int detection_bit, int state, int *next_state,float Mag_Advance,float max_angle,
					char *path, int num_bits_vq){

 AdvanceAngle gen_vector;
 static int *mem_state,*mem_output;
 static int flg_read=1;
 static int num_bits_input=NUM_BITS_INPUTS,num_bits_output=NUM_BITS_OUTPUTS;
 int size_mem;
 int index;
 int out;
 Behavior value;
 int input;
 char state_machine_file_name[300];
 int num_bits_detection = NUM_BITS_DETECTION;
 int num_bits_dest_angle = NUM_BITS_DEST_ANGLE;
 


 if(flg_read==1){
        mem_state= (int *) malloc((unsigned) NUM_MAX_MEMORY*sizeof(int));
        mem_output= (int *) malloc((unsigned) NUM_MAX_MEMORY*sizeof(int));
	sprintf(state_machine_file_name,"%s state_machine_mem.txt",path);
        size_mem=read_state_machine_robotAP(state_machine_file_name,mem_state,&num_bits_output,&num_bits_input,mem_output);

	flg_read=0;
 		}
	#ifdef DEBUG
	printf("detection_bit %d obstacle %d destinaiton %d\n",detection_bit,obs,dest);
        #endif
	
        //input = (intensity << 4) + (obs << 2) + dest;
        if (detection_bit==1){
        input =  (detection_bit << num_bits_dest_angle) + obs;
                             }
        else {
        input = (detection_bit << num_bits_dest_angle) + dest;
             }

        index = (((state) << num_bits_input) + input+1) & 0xffff;

 	*next_state=mem_state[index];
  	out=mem_output[index];
#ifdef DEBUG
 printf("index %d next_state %d out %d\n",index,*next_state,out);
#endif

 // /home/biorobotica/robotics/utilities/utilities.h //
 gen_vector=generate_output_robotAP(out,Mag_Advance,max_angle);

 //printf("Next State: %d\n", *next_state);
 return gen_vector;


}

}
