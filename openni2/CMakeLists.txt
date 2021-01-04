cmake_minimum_required( VERSION 2.8 )

set( CMAKE_BUILD_TYPE Release )
set( CMAKE_CXX_FLAGS "-std=c++11" )

# opencv 
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} "/home/yiluzhang/third_package/OpenNI-Linux-x64-2.3.0.55/Include")
link_directories("/home/yiluzhang/third_package/OpenNI-Linux-x64-2.3.0.55/Tools")

add_executable(simple_demo simple_demo.cpp )
target_link_libraries(simple_demo ${OpenCV_LIBS} libOpenNI2.so)

add_executable(open_depth_color open_depth_color.cpp )
target_link_libraries(open_depth_color ${OpenCV_LIBS} libOpenNI2.so)

add_executable(open_depth open_depth.cpp )
target_link_libraries(open_depth ${OpenCV_LIBS} libOpenNI2.so)

add_executable(open_color open_color.cpp )
target_link_libraries(open_color ${OpenCV_LIBS} libOpenNI2.so)



