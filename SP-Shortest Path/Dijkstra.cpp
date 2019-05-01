#include<iostream>
#include<algorithm>
using namespace std;

const int MAX_VERTEX_N=205;
const int INF=1e7;
bool visited[MAX_VERTEX_N];

int arcs[MAX_VERTEX_N][MAX_VERTEX_N];
int n,m;

bool CreateGraph(int n,int m)
{
    for(int i=0;i<n;i++){
        for(int j=0;j<n;j++)
            arcs[i][j]=INF;
    }//initialize
    for(int k=0;k<m;k++){
        int i,j,x;
        cin>>i>>j>>x;
        arcs[i][j]=arcs[j][i]=x;
    }
    return true;
}

int dist[MAX_VERTEX_N];
void dijkstra(int v)
{
    for(int i=0;i<n;i++)
        dist[i]=INF;
    for(int i=0;i<n;i++){
        dist[i]=arcs[v][i];
        visited[i]=false;
    }
    visited[v]=true;dist[v]=0;

    for(int i=0;i<n;i++){
        int temp=INF,u=v;
        for(int j=0;j<n;j++){
            if(!visited[j] && dist[j]<temp){
                temp=dist[j];
                u=j;
            }
        }//for j
        visited[u]=true;

        for(int k=0;k<n;k++){
            if(!visited[k] && dist[u]+arcs[u][k]<dist[k])
                dist[k]=dist[u]+arcs[u][k];
        }//for k

    }//for i
    return ;
}

int main(void)
{

    int s,t;
    while(cin>>n>>m){
        CreateGraph(n,m);
        cin>>s>>t;
        dijkstra(s);
        cout<<(dist[t]==INF?-1:dist[t])<<endl;
    }
    return 0;
}
