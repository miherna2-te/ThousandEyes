/* 
This script uses both modules selenium-webdriver and node-fetch
Importing the required dependencies.
*/
import { By, Key } from 'selenium-webdriver';
import { markers, credentials, test, driver } from 'thousandeyes';
import fetch from 'node-fetch';

// Here replace the API with the -> 
const apiUrl = 'INSERT_URL_HERE';

runScript();

async function runScript() {
  
  await configureDriver();

  var myHeaders = { 'Content-Type': 'text/xml' };

  var raw = "INSERT_BODY_HERE";

  const apiRequest = {
    method: 'POST',
    headers: myHeaders,
    body: raw };

  const apiResponse = await fetch(apiUrl, apiRequest);

  const content = await apiResponse.text();
  let output = content.replace(/\'|\"|\/|\>/gi, '    ');
  output = output.replace(/\</gi, '<br>');

  if (!apiResponse.ok) {

    throw new Error('non-200 response');
  }
  else {
    const element = driver.findElement(By.xpath('//*'))
    await driver.executeScript("arguments[0].innerHTML='" + output + "'", element);
    await driver.takeScreenshot();
  }

  async function configureDriver() {
    await driver.manage().setTimeouts({
      implicit: 7 * 1000 // If an element is not found, reattempt for this many milliseconds
    });
  }
};
