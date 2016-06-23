+----------+
|  object  |
+----------+
        .                                                                                                                                                                                                     
       /_\                                                                                                                                                                                                    
        |                    [ object ]                 [ object ]                      [ object ]                        [ object ]                   [ object ]            [ object ]          [ object ]   
        |                        .                          .                               .                                 .                            .                     .                   .        
        |                       /_\                        /_\                             /_\                               /_\                          /_\                   /_\                 /_\       
        |                        |                          |                               |                                 |                            |                     |                   |        
        |                        |                          |                               |                                 |                            |                     |                   |        
+-----------------+       +---------------+       +---------------------+       +-------------------------+       +-------------------------+       +----------------+       +----------+       +------------+
|     Settings    |       |     Logger    |       |    ScrapLottoData   |       |          Output         |       | WeightedRandomGenerator |       | TracebackError |       |   Test   |       | StyleSheet |
+-----------------+       |---------------|       |---------------------|       |-------------------------|       |-------------------------|       |----------------|       |----------|       |------------|
        |                 | level         |       | url                 |       | isMax                   |       | data                    |       | trace          |       | __init__ |       | __init__   |
        |                 | criticalFunc  |       | scrapType           |       | rowsInATicket           |       | weightsData             |       |----------------|       | runTest  |       | setColor   |
        |                 | infoFunc      |       | webData             |       | logAnatomy              |       | weightsArray            |       | __init__       |       +----------+       +------------+
        |                 | warningFunc   |       | rawData             |       | extraFileName           |       |-------------------------|       | asString       |                                        
        |                 | debugFunc     |       | totalDraws          |       | forcedNumbers           |       | __init__                |       +----------------+                                        
        |                 | errorFunc     |       | sixMonthsData       |       | applyDrawSum            |       | _setWeightsData         |                                                                 
        |                 | tracebackFunc |       | allMonthsData       |       | applyDigitSum           |       | _setWeightsArray        |                                                                 
        |                 | separatorFunc |       | sixMonthsDict       |       | applyEvens              |       | _getWeightedRandom      |                                                                 
        |                 | spaceFunc     |       | allMonthsDict       |       | applyLows               |       | getRandomNumber         |                                                                 
        |                 |---------------|       | lottoData           |       | doSevenJumps            |       | getNonWeightedRandom    |                                                                 
        |                 | onDebug       |       | sixMonthsWeightBias |       |-------------------------|       | getNaturalRandom        |                                                                 
        |                 | onWarning     |       | nbCurrentDraws      |       | __init__                |       +-------------------------+                                                                 
        |                 | onCritical    |       | nbTotalDraws        |       | _getDrawSum             |                                                                                                   
        |                 | onError       |       |---------------------|       | _getNbEvens             |                                                                                                   
        |                 | onInfo        |       | __init__            |       | _getLows                |                                                                                                   
        |                 | onTraceback   |       | _checkConnection    |       | _getDigitSum            |                                                                                                   
        |                 | onSeparator   |       | _setWebData         |       | _getSevenJumps          |                                                                                                   
        |                 | onSpace       |       | _atoi               |       | _getForcedNumbersInDraw |                                                                                                   
        |                 | warning       |       | _atof               |       | _makeOutPutString       |                                                                                                   
        |                 | info          |       | _setRawData         |       | _getTimeStamp           |                                                                                                   
        |                 | debug         |       | _setSixMonthsData   |       | _getFileName            |                                                                                                   
        |                 | error         |       | _setSixMonthsDict   |       +-------------------------+                                                                                                   
        |                 | critical      |       | _setAllmonthsData   |                                                                                                                                     
        |                 | traceback     |       | _setAllMonthsDict   |                                                                                                                                     
        |                 | _buildString  |       | _preProcessData     |                                                                                                                                     
        |                 | getLogger     |       | _setLottoData       |                                                                                                                                     
        |                 | setLevel      |       | getLottoData        |                                                                                                                                     
        |                 | getLevel      |       +---------------------+                                                                                                                                     
        |                 | addSeparator  |                                                                                                                                                                   
        |                 | addSpace      |                                                                                                                                                                   
                          +---------------+                                                                                                                                                                   
        .          
       /_\         
        |          
        |          
        |          
        |          
        |          
+-----------------+
|  MainAlgorithm  |
|-----------------|
| sm              |
| dsm             |
| nbEven          |
| nbLow           |
| validation      |
| gen             |
| nbSevenJumps    |
| qThread         |
| winningDraw     |
| outStr          |
|-----------------|
| __init__        |
| _getDraw        |
| _getSevenJumps  |
| _setDrawAnatomy |
| _validateDraw   |
| runAlg          |
| output          |
+-----------------+
                 
                 
                 
                 
+---------------+
| QtGui.QWidget |
+---------------+
                .                   
               /_\                  
                |                   
                |                   
                |                   
                |                   
                |                   
+----------------------------------+
|           MainWidgetUI           |
+----------------------------------+
                .                                              
               /_\                                             
                |                                              
                |                                              
                |                                              
                |                                              
                |                                              
+----------------------------------+                           
|            MainWidget            |                           
|----------------------------------|                           
| _lottoTypes                      |  ---->  [ ProgressWidget ]
| _forcedNumbers                   |  ---->  [ RulesWidget ]   
| _outDir                          |  ---->  [ time.time ]     
| _isLottoMax                      |  ---->  [ SettingsWidget ]
| _nbTickets                       |  ---->  [ RunAlgTask ]    
| _doSevenJumps                    |                           
| _scrapType                       |                           
| _nbFromForced                    |                           
| _logAnatomy                      |                           
| _logSettings                     |                           
| _iter                            |                           
| _start                           |                           
| _end                             |                           
| _settings                        |                           
| _rules                           |                           
| sw                               |                           
| rw                               |                           
| rat                              |                           
| pw                               |                           
|----------------------------------|                           
| __init__                         |                           
| _initData                        |                           
| _initUI                          |                           
| _initWidgets                     |                           
| _updateForcedNumberLineEdit      |                           
| _connectSignals                  |                           
| _lottoTypeComboBoxIndexChanged   |                           
| _nbTicketsSpinBoxValueChanged    |                           
| _selectOutPathBtnOnClicked       |                           
| _clearOutPathBtnOnClicked        |                           
| _connectRadioBtn                 |                           
| _radioBtnClickedMappedSlot       |                           
| _sevenJumpsCheckBoxOnClicked     |                           
| _logAnatomyCheckBoxOnClicked     |                           
| _logSettingsCheckBoxOnClicked    |                           
| _settingsBtnOnClicked            |                           
| _rulesBtnOnClicked               |                           
| _noNumberCheckBoxOnClicked       |                           
| _connectCheckBox                 |                           
| _checkBoxClickedMappedSlot       |                           
| _nbFromForcedSpinBoxValueChanged |                           
| _clearTextBtnOnClicked           |                           
| _copyBtnOnClicked                |                           
| _isNetworkAvailable              |                           
| _generateBtnOnClicked            |                           
| _informOfUpdate                  |                           
| _informOfFinished                |                           
| _informOfRanOutOfLoops           |                           
| _resetBtnOnClicked               |                           
| _cancelBtnOnClicked              |                           
+----------------------------------+                           
                      
                      
                      
                      
+--------------------+
|   QtCore.QThread   |
+--------------------+
         .            
        /_\           
         |            
         |            
         |            
         |            
         |            
+--------------------+
|     RunAlgTask     |
|--------------------|
| result             |
| lottoIsMax         |
| writeDirPath       |
| write              |
| scrapType          |
| logAnatomy         |
| nbTickets          |
| doSevenJumps       |
| forcedNumbers      |
| nbFromForcedRandom |
| applyDrawSum       |
| applyDigitSum      |
| applyEvens         |
| applyLows          |
| drawSumMin         |
| drawSumMax         |
| digitSumMin        |
| digitSumMax        |
| nbEvens            |
| nbLows             |
|--------------------|
| __init__           |
| runRat             |
| run                |
+--------------------+
                     
                     
                     
                     
+-------------------+
| QtGui.QMainWindow |
+-------------------+
        .                                  
       /_\                                 
        |                                  
        |                                  
        |                                  
        |                                  
        |                                  
+------------------+                       
|    MainWindow    |                       
|------------------|                       
| _mainWidget      |  ---->  [ MainWidget ]
| _presetsMenu     |                       
|------------------|                       
| __init__         |                       
| _onAboutAction   |                       
| _onLicenseAction |                       
| _onSaveAction    |                       
| _getSettings     |                       
| _onLoadAction    |                       
| _applySettings   |                       
+------------------+                       
                 
                 
                 
                 
+---------------+
| QtGui.QDialog |
+---------------+
      .                                                                                                            
     /_\                                                                                                           
      |               [ QtGui.QDialog ]         [ QtGui.QDialog ]       [ QtGui.QDialog ]        [ QtGui.QDialog ] 
      |                       .                       .                        .                        .          
      |                      /_\                     /_\                      /_\                      /_\         
      |                       |                       |                        |                        |          
      |                       |                       |                        |                        |          
+-------------+       +-----------------+       +-------------+         +----------------+       +----------------+
| AboutWidget |       |  LicenseWidget  |       | RulesWidget |         | SettingsWidget |       | ProgressWidget |
|-------------|       |-----------------|       +-------------+         +----------------+       +----------------+
| pic         |       | text            |                                                                          
|-------------|       | textEdit        |                                                                          
| __init__    |       | okBtn           |                                                                          
| _initUI     |       | _vLayout        |                                                                          
+-------------+       |-----------------|                                                                          
                      | __init__        |                                                                          
                      | _initUI         |                                                                          
                      | _connectSignals |                                                                          
                      | _okBtnOnClicked |                                                                          
                      +-----------------+                                                                          
             
             
             
             
+-----------+
| time.time |
+-----------+
