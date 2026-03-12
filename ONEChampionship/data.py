onechampionship_Teams = [
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

from onechampionship.models import Type
Teams = [Type(name=type) for type in onechampionship_Teams]