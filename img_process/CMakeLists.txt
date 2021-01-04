cmake_minimum_required( VERSION 2.8 )

set( CMAKE_BUILD_TYPE Release )
set( CMAKE_CXX_FLAGS "-std=c++11" )

# opencv 
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS})

add_executable(change_pixel change_pixel.cpp )
target_link_libraries(change_pixel ${OpenCV_LIBS})

#add_executable(open_depth_color open_depth_color.cpp )
#target_link_libraries(open_depth_color ${OpenCV_LIBS} libOpenNI2.so)

#add_executable(open_depth open_depth.cpp )
#target_link_libraries(open_depth ${OpenCV_LIBS} libOpenNI2.so)

#add_executable(open_color open_color.cpp )
#target_link_libraries(open_color ${OpenCV_LIBS} libOpenNI2.so)



