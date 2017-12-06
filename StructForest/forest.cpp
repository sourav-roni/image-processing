#include <cv.h>
#include <highgui.h>
#include <opencv2/ximgproc.hpp>
#include "opencv2/highgui.hpp"
#include "opencv2/core/utility.hpp"
#include <bits/stdc++.h>
#include <dirent.h>
#include <iostream>
#include <fstream>
#include <iterator>
using namespace cv;
using namespace std;
using namespace cv::ximgproc;
   
int main( int argc, const char** argv )
{
    DIR *pDIR,*outDIR;
    string modelFilename = "model.yml";
    dirent *entry;
    string inFilename="",temp="";
    ifstream inFile;
    string outFilename ="";
    if( pDIR=opendir("/home/vedant/Desktop/IP_opencv/forest/OriginalImage") )
    {
        while(entry = readdir(pDIR))
        {
            if( strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..") != 0 )
            {
                //cout << entry->d_name << "\n";
                inFilename = "/home/vedant/Desktop/IP_opencv/forest/OriginalImage/";
                inFilename += entry->d_name; 
                temp = entry->d_name;
                outFilename = "/home/vedant/Desktop/IP_opencv/forest/OriginalImageOutput/";
                int len = temp.length();
                for(int i=0;i<len;i++)
                {
                    if(temp[i] == '.')
                        break;
                    outFilename += temp[i];
                }
                
                outFilename += "_out.jpg";
                //cout<<outFilename<<endl;
                
                cv::Mat image = cv::imread(inFilename, 1);
                if ( image.empty() )
                {
                    printf("Cannot read image file: %s\n", inFilename.c_str());
                    continue;
                }

                image.convertTo(image, cv::DataType<float>::type, 1/255.0);
                cv::Mat edges(image.size(), image.type());
                cv::Ptr<StructuredEdgeDetection> pDollar =
                    createStructuredEdgeDetection(modelFilename);
                pDollar->detectEdges(image, edges);

                if ( outFilename == "" )
                {
                    cv::namedWindow("edges", 1);
                    cv::imshow("edges", edges);
                    cv::waitKey(0);
                }
                else
                    cv::imwrite(outFilename, 255*edges); 
            }
        }
        closedir(pDIR);
    }
    return 0;
}
