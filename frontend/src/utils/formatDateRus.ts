export function formatDateToRus(date: string | Date): string {
   // Преобразуем строку в объект Date, если это строка
  const dateObj = new Date(date);

  // Используем Intl.DateTimeFormat для форматирования даты с сокращением месяца
  const options: Intl.DateTimeFormatOptions = {
    day: 'numeric',
    month: 'short',  // Сокращение месяца
  };

  // Форматируем дату с помощью локали 'ru-RU' для русского языка
  const formattedDate = new Intl.DateTimeFormat('ru-RU', options).format(dateObj);

  // Возвращаем отформатированную дату без года
  return formattedDate;
}
