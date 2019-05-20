#include <iostream>

int main(){
    for(int x = 0; x < 8; x++){
        for(int y = 0; y < 8; y++){
            if( x+1 < 8){
                std::cout << "linked([" << x << "," << y << "],[" << x+1 << "," << y << "]).\n";
            }
            if( x-1 >= 0){
                std::cout << "linked([" << x << "," << y << "],[" << x-1 << "," << y << "]).\n";
            }
            if( y+1 < 8){
                std::cout << "linked([" << x << "," << y << "],[" << x << "," << y+1 << "]).\n";
            }
            if( y-1 >= 0){
                std::cout << "linked([" << x << "," << y << "],[" << x << "," << y-1 << "]).\n";   
            }
        }
    }
}