$(document).ready(function() {
    $('#date_sale').datepicker({
        format: 'dd/mm/yyyy', // Formato de data
        autoclose: true,     // Fecha o calendário automaticamente após a seleção
        todayHighlight: true, // Destaca o dia atual
        language: 'pt-BR'
    });
});

$(document).ready(function() {
    $('#date_purchase').datepicker({
        format: 'dd/mm/yyyy', // Formato de data
        autoclose: true,     // Fecha o calendário automaticamente após a seleção
        todayHighlight: true, // Destaca o dia atual
        language: 'pt-BR',
    });
});

$(document).ready(function() {
    $('#payment_method').datepicker({
        format: 'dd/mm/yyyy', // Formato de data
        autoclose: true,     // Fecha o calendário automaticamente após a seleção
        todayHighlight: true, // Destaca o dia atual
        // startDate: '+0d',
        language: 'pt-BR'
    });
});
$(document).ready(function() {
    $('#date_init').datepicker({
        format: 'dd/mm/yyyy', // Formato de data
        autoclose: true,     // Fecha o calendário automaticamente após a seleção
        todayHighlight: true, // Destaca o dia atual
        // startDate: '+0d',
        language: 'pt-BR'
    });
});
$(document).ready(function () {
    $('#date_init_planned_account').datepicker({
      format: "mm/yyyy",
      startView: "months",
      minViewMode: "months",
      autoclose: true,
      todayHighlight: true,
      language: "pt-BR"
    });
  });
$(document).ready(function() {
    $('#tax_date_init').datepicker({
        format: 'dd/mm/yyyy', // Formato de data
        autoclose: true,     // Fecha o calendário automaticamente após a seleção
        todayHighlight: true, // Destaca o dia atual
        // startDate: '+0d',
        language: 'pt-BR'
    });
});

$(document).ready(function() {
    $('#freight_date_init').datepicker({
        format: 'dd/mm/yyyy', // Formato de data
        autoclose: true,     // Fecha o calendário automaticamente após a seleção
        todayHighlight: true, // Destaca o dia atual
        // startDate: '+0d',
        language: 'pt-BR'
    });
});

$(document).ready(function() {
    $('#romaneio_date_init').datepicker({
        format: 'dd/mm/yyyy', // Formato de data
        autoclose: true,     // Fecha o calendário automaticamente após a seleção
        todayHighlight: true, // Destaca o dia atual
        // startDate: '+0d',
        language: 'pt-BR'
    });
});

$(document).ready(function() {
    $('#expiration_date').datepicker({
        format: 'dd/mm/yyyy', // Formato de data
        autoclose: true,     // Fecha o calendário automaticamente após a seleção
        todayHighlight: true, // Destaca o dia atual
        // startDate: '+0d',
        language: 'pt-BR'
    });
});
$(document).ready(function() {
    // const dateStr = document.getElementById('id_date_init')
    $('#date_account').datepicker({
        format: 'dd/mm/yyyy', // Formato de data
        autoclose: true,     // Fecha o calendário automaticamente após a seleção
        todayHighlight: true, // Destaca o dia atual
        // startDate: '+0d',
        language: 'pt-BR'
    });
    // convert_date(dateStr.value)
    
});



function convert_date(dateStr){
    const input = document.getElementById('id_date_init')
    const convertToDate = (dateStr) => {
        console.log('dateStr',dateStr)
        const [year1, year2, daymonth ] = dateStr.split('/')
        const real_mes = String(daymonth) 
        console.log('ano',year1+year2)
        console.log('mes',real_mes.substring(0,2))
        console.log('dia', real_mes.substring(2,4))
        return new Date(year1+year2, real_mes.substring(0,2) - 1, real_mes.substring(2,4)); // Mês no JavaScript começa do 0
    };
    // console.log("convertToDate: ",`${convertToDate.getDate().toString().padStart(2, '0')}/` +
    // `${(convertToDate.getMonth() + 1).toString().padStart(2, '0')}/` +
    // `${convertToDate.getFullYear()}`)
    const inputDate = dateStr;
    // Converter a data inicial
    const startDate = convertToDate(inputDate);
    // const startDate = new Date(inputDate);
    // Verifica se a data foi convertida corretamente
    if (isNaN(startDate.getTime())) {
        console.error('Data inválida');
        return;
    } 

    input.value = `${startDate.getDate().toString().padStart(2, '0')}/${(startDate.getMonth() + 1).toString().padStart(2, '0')}/${startDate.getFullYear()}`  
    console.log(`${startDate.getDate().toString().padStart(2, '0')}/${(startDate.getMonth() + 1).toString().padStart(2, '0')}/${startDate.getFullYear()}`)
}