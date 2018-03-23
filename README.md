## 2016 PHM challenge society  

The competition is on the data science lesson in NCTU, 2017.  
Competition website: https://www.phmsociety.org/events/conference/phm/16/data-challenge  
***  
    
#### System and Data Description
***This year’s challenge is focused on the combination of physics-based modeling and statistical approaches for prediction. It is not required that the solution you select use a physics-based modeling approach. However, additional points will be given to those approaches that provide some physical connection to the data such as health states of various components, relationship between data and model parameters / states, etc.***  
  
***The system under investigation is a wafer Chemical-Mechanical Planarization (CMP) tool that removes material from the surface of the wafer through a polishing process. Figure 1 depicts the CMP process components and operation. The CMP tool is composed of the following components:***   
>a rotating table used to hold a polishing pad  
>a replaceable polishing pad which is attached to the table  
>a translating and rotating wafer carrier used to hold the wafer  
>a slurry dispenser  
>a translating and rotating dresser used to condition a polishing pad.  
![alt](https://www.phmsociety.org/sites/phmsociety.org/files/Fig1PHM16DataChallenge.png)  
***Figure 1: Chemical Mechanical Planarization (Polishing) of wafer. This process removes material from wafer surface.***
  
***A wafer is placed on the underside of a wafer carrier in the CMP tool, the CMP tool recipe is set (e.g. set-points for speeds, forces, polish time, etc.), and the polishing process is started. During the polishing process, the wafer is pressed against a polishing pad and both the wafer / wafer carrier and polishing pad / table are rotated in the same direction. A slurry composed of abrasive materials and chemicals are dispensed onto the pad during the polishing process. After polishing is completed, the polishing pad may be conditioned to improve its polishing properties by using a dresser. The dresser is typically composed of a hard material such as diamond that is pressed across the pad to roughen the pad’s surface to prepare it for future polishing operations.***  
  
***During the polishing process, the polishing pad’s ability to remove material is diminished. Over time, the polishing pad has to be replaced with a new pad. Similarly, the dresser’s capability to roughen the polishing pads is also reduced after successive conditioning operations and after a while the dresser must be replaced.***  
  
#### Objective  
The primary objective of this challenge is to predict polishing removal rate of material from a wafer using physics-based modeling methods and the data provided. The condition of the polishing pad and dresser change over time as they are being used. If these states can be estimated, then polishing time estimates can possibly be improved.

Data Description
Training and test data sets are provided to you to establish your methods. The training data represents data collected during various runs of the CMP tool for specified wafers over time. Data is given in the Table 1 format described below. Each row of the data represents an instance of all measurement variables at any given time. An average rate of material removal from a wafer is given separately in Table 2, which has a corresponding wafer identification number and stage. The average rate of removal was determined from measurements of the thickness of the material before and after CMP polishing. 
The 'rotational speed' is the label what we want to predict.  


