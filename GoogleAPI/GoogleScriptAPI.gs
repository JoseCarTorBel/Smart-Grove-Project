function doGet(){
 textOutput = ContentService.createTextOutput(JSON.stringify(getData()));
 return textOutput;
}

function getData() {
  spreadsheetId="1XjSgEeqwPTAHUzqUTZfFDrkH1L6FZWVnqf_mrH37dRw"
  sheet="BBDD"
  var rangeName = sheet+'!A1:Z';  
  var values = Sheets.Spreadsheets.Values.get(spreadsheetId, rangeName).values;
 
  if (!values) {
    return {error: 'No data found'}
  } else {
    
    var responseJson = [];
    
    for (var row = 1; row < values.length; row++) {
      var item ={};
      
      for(var column = 0; column < 26; column++){
        item[values[0][column]] = values[row][column]
      }
      responseJson.push(item);
    }
    return responseJson;
  }
}


