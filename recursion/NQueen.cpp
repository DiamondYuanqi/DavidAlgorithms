//
// Created by 袁琦 on 2020/11/26.
//
#include<iostream>
#include<cmath>
using namespace std;
int N;
int queenPos[100];
void NQueen(int k){//在0～K-1行皇后已经摆好的情况下，摆第k行及其后第皇后
    int i;
    if(k==N){//N个皇后已经摆好
        for(i=0;i<N;i++){
            cout<< queenPos[i]+1<<" ";//输出结果表示：从第0行开始摆放 所以+1是第i个
        }   //queenPos[i] 表示第i行摆好的皇后的列号 i
        cout<<endl;
        return;
    }
    for(i=0;i<N;i++){//逐个尝试第k个皇后所有可能的位置 列i
        int j;//判断列i是否可行 i即k  与从0～k-1行的皇后是否冲突
        for(j=0;j<k;j++){//和已经摆好的k个皇后的位置进行比较，看是否冲突
            if(queenPos[j]==i||abs(queenPos[j]-i==abs(k-j)){//行列｜｜斜着
                break;//冲突，测试下一个位置 将第j行皇后摆在第i列 看是否可行
            }
        }
        if(j==k) {//当前选的位置i 不冲突
            queenPos[k] = i;//将第k个皇后摆放在位置i
            NQueen(k + 1);//第一次递归i从0到1 第二次递归从1到2
            //如果当前递归无解，返回到上一行，跳出当前循环 进入for（i=0;i<N;i++)试探皇后下一个列的位置
        }
    }//for（i=0;i<N;i++)
}
int main(){
    cin>>N;
    NQueen(0);//从第0行开始摆皇后
    return 0;
}