ONEChampionship_Teams = [
  "อะตอมเวต",
  "สตรอว์เวต",
  "ฟลายเวต",
  "แบนตัมเวต",
  "เฟเธอร์เวต",
  "ไลต์เวต",
  "เวลเตอร์เวต",
  "มิดเดิลเวต",
  "ไลต์เฮฟวีเวต",
  "เฮฟวีเวต"
]

from ONEChampionship.models import Type
Teams = [Type(name=type) for type in ONEChampionship_Teams]