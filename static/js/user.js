var pw = document.getElementById('password')
var confirmPW = document.getElementById('pwCheck')

function isValidFormPassword(pw) {
 var check = /^(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{6,16}$/;

 if (!check.test(pw))     {
        return false;
    }

 if (pw.length < 6 || pw.length > 16) {
  return false;
 }

    return true;
}
